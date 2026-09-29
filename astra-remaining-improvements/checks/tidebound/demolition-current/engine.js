"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.newGame = newGame;
exports.getIslandStats = getIslandStats;
exports.getPlacementError = getPlacementError;
exports.placeBuilding = placeBuilding;
exports.removeBuilding = removeBuilding;
exports.research = research;
exports.buildShip = buildShip;
exports.exploreIsland = exploreIsland;
exports.settleIsland = settleIsland;
exports.trade = trade;
exports.createRoute = createRoute;
exports.tick = tick;
exports.getObjectives = getObjectives;
exports.serializeGame = serializeGame;
exports.parseSave = parseSave;
const data_1 = require("./data");
const types_1 = require("./types");
const inventory = (values = {}) => Object.assign(Object.fromEntries(types_1.RESOURCES.map(r => [r, 0])), values);
const total = (inv) => types_1.RESOURCES.reduce((n, r) => n + inv[r], 0);
const sum = (items) => Object.values(items).reduce((a, b) => a + (b ?? 0), 0);
const has = (inv, cost) => types_1.RESOURCES.every(r => inv[r] >= (cost[r] ?? 0));
const pay = (inv, cost) => { for (const r of types_1.RESOURCES)
    inv[r] -= cost[r] ?? 0; };
const result = (ok, message) => ({ ok, message });
const id = (s, prefix) => `${prefix}-${s.nextId++}`;
const note = (s, text, tone = 'info') => { s.log.unshift({ id: s.nextId++, time: s.time, text, tone }); s.log = s.log.slice(0, 70); };
const hash = (s) => { let h = 2166136261; for (let i = 0; i < s.length; i++)
    h = Math.imul(h ^ s.charCodeAt(i), 16777619); return h >>> 0; };
const random = (seed) => { let h = hash(seed); return () => { h += 0x6D2B79F5; let t = Math.imul(h ^ (h >>> 15), 1 | h); t ^= t + Math.imul(t ^ (t >>> 7), 61 | t); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
const active = (i, t) => i.buildings.filter(b => b.type === t && b.enabled).length;
const coastal = (i, x, z) => [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dz]) => !i.tiles.some(t => t.x === x + dx && t.z === z + dz));
const portTile = (i) => [...i.tiles].sort((a, b) => b.x - a.x || Math.abs(a.z) - Math.abs(b.z))[0];
const port = (i) => ({ x: i.x + i.radius + 3, z: i.z });
function newGame(seed = 'tidebound-001') {
    seed = seed.trim().slice(0, 200) || 'tidebound-001';
    const rng = random(seed);
    const s = { version: 1, seed, time: 0, speed: 1, gold: 900, knowledge: 28, islands: [], ships: [], routes: [], researched: [], events: [], log: [], nextId: 1, nextEvent: 240, victory: false, tutorialStep: 0, settings: { music: .25, effects: .5, reducedMotion: false, shadows: true } };
    const names = ['Hearthwater', 'Verdant Cay', 'Ember Reach', 'Palmhaven', 'Silverstrand', 'Cinderwatch', 'Mistwood'];
    const positions = [[0, 0], [43, -14], [18, 46], [-35, 28], [-38, -27], [7, -47], [62, 34]];
    for (let n = 0; n < 7; n++) {
        const biome = ['temperate', 'tropical', 'volcanic'][n % 3];
        const radius = n === 0 ? 13 : 11 + rng() * 3;
        const i = { id: `island-${n}`, name: names[n], biome, x: positions[n][0], z: positions[n][1], radius, tiles: [], discovered: n === 0 || n >= 3, settled: n === 0, npc: n >= 3 && n <= 5, inventory: inventory(), buildings: [] };
        for (let x = -7; x <= 7; x++)
            for (let z = -7; z <= 7; z++) {
                const d = Math.hypot(x, z) * data_1.TILE_SPACING;
                if (d < radius - 1 + (rng() - .5) * 1.4)
                    i.tiles.push({ x, z, height: .45 + Math.max(0, 1 - d / radius) * .7 + rng() * .18, kind: d > radius - 3 ? 'sand' : biome === 'volcanic' && rng() > .45 ? 'rock' : 'grass' });
            }
        if (i.npc) {
            i.inventory = inventory({ wood: 280, stone: 280, fish: 200, grain: 200, planks: 150, bricks: 150, iron: 100, tools: 80, cloth: 120, tea: 100 });
            const p = portTile(i);
            i.buildings.push({ id: id(s, 'building'), type: 'harbor', x: p.x, z: p.z, enabled: true, progress: 0, status: 'Trading port' });
        }
        s.islands.push(i);
    }
    const home = s.islands[0];
    home.inventory = inventory({ wood: 85, stone: 55, fish: 65, grain: 30, planks: 35, bricks: 20, iron: 0, tools: 8, cloth: 12, tea: 0 });
    const p = portTile(home);
    for (const [type, x, z] of [['harbor', p.x, p.z], ['cottage', 0, 0], ['lumberyard', -2, 0], ['warehouse', 0, -2], ['fishery', p.x, p.z === 0 ? 1 : p.z - 1]]) {
        let tx = x, tz = z;
        if (!home.tiles.some(t => t.x === tx && t.z === tz) || home.buildings.some(b => b.x === tx && b.z === tz) || data_1.BUILDINGS[type].coastal && !coastal(home, tx, tz)) {
            const tile = home.tiles.find(t => !home.buildings.some(b => b.x === t.x && b.z === t.z) && (!data_1.BUILDINGS[type].coastal || coastal(home, t.x, t.z)));
            tx = tile.x;
            tz = tile.z;
        }
        home.buildings.push({ id: id(s, 'building'), type, x: tx, z: tz, enabled: true, progress: 0, status: 'Ready' });
    }
    const hp = port(home);
    s.ships.push({ id: id(s, 'ship'), name: 'Wayfarer', home: home.id, ...hp, cargo: inventory(), capacity: 60, routeId: null, status: 'Idle at Hearthwater' });
    note(s, 'Welcome to Hearthwater. Build homes, feed your settlers, and connect the islands.', 'good');
    return s;
}
function getIslandStats(s, islandId) {
    const i = s.islands.find(i => i.id === islandId);
    if (!i)
        return { population: 0, workers: 0, employed: 0, happiness: 0, capacity: 0, food: 0, foodRate: 0 };
    const population = active(i, 'cottage') * 12;
    const workers = Math.floor(population * .65);
    const employed = i.buildings.filter(b => b.enabled).reduce((n, b) => n + data_1.BUILDINGS[b.type].workers, 0);
    const food = i.inventory.fish + i.inventory.grain;
    const happiness = Math.min(100, Math.max(15, (food > population * .1 ? 65 : 22) + (i.inventory.cloth > .1 ? 8 : 0) + (i.inventory.tea > .1 ? 8 : 0) + Math.min(2, active(i, 'market')) * 8 + (s.events.some(e => e.type === 'festival') ? 12 : 0)));
    const labor = employed ? Math.min(1, workers / employed) : 1;
    let foodRate = -population * .007;
    for (const b of i.buildings.filter(b => b.enabled))
        if (b.type === 'farm' || b.type === 'fishery') {
            const d = data_1.BUILDINGS[b.type];
            foodRate += sum(d.output) / d.duration * labor * productionFactor(s, i, b.type);
        }
    return { population, workers, employed: Math.min(workers, employed), happiness, capacity: 400 + active(i, 'warehouse') * 600 + (i.npc ? 5000 : 0), food, foodRate };
}
function getPlacementError(s, islandId, type, x, z) {
    const i = s.islands.find(i => i.id === islandId), d = data_1.BUILDINGS[type];
    if (!i || !i.settled || i.npc)
        return 'Settle this island before building.';
    if (!Object.hasOwn(data_1.BUILDINGS, type))
        return 'Unknown building.';
    if (!Number.isInteger(x) || !Number.isInteger(z) || !i.tiles.some(t => t.x === x && t.z === z))
        return 'Choose a land tile.';
    if (i.buildings.some(b => b.x === x && b.z === z))
        return 'This tile already has a building.';
    if (d.unlock && !s.researched.includes(d.unlock))
        return `Research ${data_1.TECHNOLOGIES.find(t => t.id === d.unlock)?.name} first.`;
    if (d.coastal && !coastal(i, x, z))
        return 'This building requires a coastal tile.';
    if (s.gold < d.gold)
        return `Requires ${d.gold} gold.`;
    if (!has(i.inventory, d.cost))
        return `Missing materials: ${types_1.RESOURCES.filter(r => i.inventory[r] < (d.cost[r] ?? 0)).map(r => `${Math.ceil((d.cost[r] ?? 0) - i.inventory[r])} ${data_1.RESOURCE_META[r].name}`).join(', ')}.`;
    return null;
}
function placeBuilding(s, islandId, type, x, z) {
    const error = getPlacementError(s, islandId, type, x, z);
    if (error)
        return result(false, error);
    const i = s.islands.find(i => i.id === islandId), d = data_1.BUILDINGS[type];
    pay(i.inventory, d.cost);
    s.gold -= d.gold;
    i.buildings.push({ id: id(s, 'building'), type, x, z, enabled: true, progress: 0, status: 'Ready' });
    note(s, `${d.name} built on ${i.name}.`, 'good');
    return result(true, `${d.name} constructed.`);
}
function removeBuilding(s, islandId, buildingId) {
    const i = s.islands.find(i => i.id === islandId);
    const b = i?.buildings.find(b => b.id === buildingId);
    if (!i || !i.settled || !b)
        return result(false, 'Building not found.');
    if (b.type === 'harbor' && b.enabled && active(i, 'harbor') <= 1)
        return result(false, 'Keep at least one active harbor on each settled island.');
    if (b.type === 'harbor' && i.buildings.filter(building => building.type === 'harbor').length <= 1)
        return result(false, 'Keep at least one harbor on each settled island.');
    if (b.type === 'warehouse' && b.enabled && total(i.inventory) > getIslandStats(s, i.id).capacity - 600)
        return result(false, 'Move goods before removing this warehouse.');
    // Pausing a warehouse can leave existing goods above the reduced capacity.
    // Refunds must never become negative and consume those existing goods.
    i.buildings = i.buildings.filter(o => o.id !== buildingId);
    let room = Math.max(0, getIslandStats(s, i.id).capacity - total(i.inventory));
    for (const r of types_1.RESOURCES) {
        const refund = Math.min(room, Math.floor((data_1.BUILDINGS[b.type].cost[r] ?? 0) * .5));
        i.inventory[r] += refund;
        room -= refund;
    }
    return result(true, 'Building removed; half its materials recovered where storage permits.');
}
function research(s, techId) {
    const t = data_1.TECHNOLOGIES.find(t => t.id === techId);
    if (!t)
        return result(false, 'Unknown technology.');
    if (s.researched.includes(t.id))
        return result(false, 'Already researched.');
    if (t.requires.some(r => !s.researched.includes(r)))
        return result(false, 'Complete the prerequisite research first.');
    if (s.knowledge < t.cost)
        return result(false, `Requires ${t.cost} knowledge.`);
    s.knowledge -= t.cost;
    s.researched.push(t.id);
    note(s, `${t.name} researched.`, 'good');
    return result(true, `${t.name} unlocked.`);
}
function buildShip(s, islandId) {
    const i = s.islands.find(i => i.id === islandId);
    if (!i?.settled || !active(i, 'shipyard'))
        return result(false, 'Build a shipyard here first.');
    const cost = { planks: 20, cloth: 8 };
    if (s.gold < 90 || !has(i.inventory, cost))
        return result(false, 'A ship requires 90 gold, 20 planks, and 8 cloth.');
    pay(i.inventory, cost);
    s.gold -= 90;
    const names = ['Albatross', 'North Star', 'Kestrel', 'Sea Lantern', 'Wanderer'];
    s.ships.push({ id: id(s, 'ship'), name: names[(s.ships.length - 1) % names.length], home: i.id, ...port(i), cargo: inventory(), capacity: 60, routeId: null, status: `Idle at ${i.name}` });
    note(s, 'A new cargo ship joins your fleet.', 'good');
    return result(true, 'Ship launched.');
}
function exploreIsland(s, islandId) {
    const i = s.islands.find(i => i.id === islandId);
    if (!i)
        return result(false, 'Island not found.');
    if (i.discovered)
        return result(false, 'Island already charted.');
    if (s.gold < 35)
        return result(false, 'An expedition requires 35 gold.');
    if (!s.ships.length)
        return result(false, 'An expedition requires a ship.');
    s.gold -= 35;
    i.discovered = true;
    s.knowledge += 8;
    note(s, `${i.name} charted. The expedition returned with 8 knowledge.`, 'good');
    return result(true, `${i.name} explored.`);
}
function settleIsland(s, islandId) {
    const i = s.islands.find(i => i.id === islandId);
    if (!i?.discovered)
        return result(false, 'Explore this island first.');
    if (i.npc || i.settled)
        return result(false, 'This island is already inhabited.');
    if (!s.researched.includes('navigation'))
        return result(false, 'Research Celestial Navigation before founding a new island settlement.');
    const home = s.islands.find(i => i.settled);
    const cost = { wood: 35, stone: 20, fish: 15 };
    if (s.gold < 120 || !has(home.inventory, cost))
        return result(false, 'A colony expedition needs 120 gold, 35 timber, 20 stone, and 15 fish at Hearthwater.');
    pay(home.inventory, cost);
    s.gold -= 120;
    i.settled = true;
    i.inventory = inventory({ wood: 25, stone: 15, fish: 30, planks: 10 });
    const p = portTile(i);
    i.buildings.push({ id: id(s, 'building'), type: 'harbor', x: p.x, z: p.z, enabled: true, progress: 0, status: 'Ready' }, { id: id(s, 'building'), type: 'cottage', x: 0, z: 0, enabled: true, progress: 0, status: 'Ready' });
    note(s, `A new settlement founded on ${i.name}.`, 'good');
    return result(true, `${i.name} settled with a harbor, homes, and supplies.`);
}
function trade(s, islandId, resource, amount, side) {
    const i = s.islands.find(i => i.id === islandId);
    if (!i?.settled || !active(i, 'harbor'))
        return result(false, 'Trade requires a harbor on your island.');
    if (!types_1.RESOURCES.includes(resource) || !Number.isInteger(amount) || amount <= 0 || amount > 10000)
        return result(false, 'Choose a positive whole amount.');
    if (side !== 'buy' && side !== 'sell')
        return result(false, 'Unknown trade direction.');
    const price = data_1.RESOURCE_META[resource].price * (side === 'buy' ? (s.researched.includes('commerce') ? 1.1 : 1.25) : .7);
    if (side === 'buy') {
        if (s.gold + 1e-8 < price * amount)
            return result(false, 'Not enough gold.');
        if (total(i.inventory) + amount > getIslandStats(s, i.id).capacity)
            return result(false, 'Not enough storage.');
        s.gold = Math.max(0, s.gold - price * amount);
        i.inventory[resource] += amount;
    }
    else {
        if (i.inventory[resource] < amount)
            return result(false, 'Not enough goods.');
        i.inventory[resource] -= amount;
        s.gold += price * amount;
    }
    return result(true, `${side === 'buy' ? 'Bought' : 'Sold'} ${amount} ${data_1.RESOURCE_META[resource].name}.`);
}
const paths = new Map();
function routePath(s, from, to) {
    const key = `${s.seed}:${from.id}:${to.id}:${s.islands.map(i => `${i.x},${i.z},${i.radius}`).join(';')}`;
    const cached = paths.get(key);
    if (cached)
        return cached;
    // Visibility-graph shortest path: no segment cuts through the conservative circular shoreline.
    const start = port(from), end = port(to), step = 3;
    const clear = (a, b) => s.islands.every(i => { const dx = b.x - a.x, dz = b.z - a.z; const t = Math.max(0, Math.min(1, ((i.x - a.x) * dx + (i.z - a.z) * dz) / (dx * dx + dz * dz || 1))); return Math.hypot(a.x + t * dx - i.x, a.z + t * dz - i.z) >= i.radius + 1; });
    if (clear(start, end)) {
        const p = [start, end];
        paths.set(key, p);
        return p;
    }
    const nodes = [start, end];
    for (const i of s.islands)
        for (let a = 0; a < 24; a++) {
            const angle = a / 24 * Math.PI * 2;
            const p = { x: i.x + Math.cos(angle) * (i.radius + step), z: i.z + Math.sin(angle) * (i.radius + step) };
            if (s.islands.every(j => Math.hypot(p.x - j.x, p.z - j.z) > j.radius + 1))
                nodes.push(p);
        }
    const dist = nodes.map(() => Infinity), prev = nodes.map(() => -1), open = new Set(nodes.map((_, n) => n));
    dist[0] = 0;
    while (open.size) {
        let u = -1, best = Infinity;
        for (const n of open)
            if (dist[n] < best) {
                u = n;
                best = dist[n];
            }
        if (u < 0 || u === 1)
            break;
        open.delete(u);
        for (const v of open)
            if (clear(nodes[u], nodes[v])) {
                const d = dist[u] + Math.hypot(nodes[u].x - nodes[v].x, nodes[u].z - nodes[v].z);
                if (d < dist[v]) {
                    dist[v] = d;
                    prev[v] = u;
                }
            }
    }
    const path = [];
    let n = 1;
    while (n >= 0) {
        path.unshift(nodes[n]);
        n = prev[n];
    }
    if (path.length < 2)
        throw new Error('No navigable sea route found.');
    paths.set(key, path);
    if (paths.size > 200)
        paths.delete(paths.keys().next().value);
    return path;
}
function loadCargo(s, ship, i, r, amount) {
    if (!r)
        return;
    let units = Math.min(amount, i.inventory[r], ship.capacity - total(ship.cargo));
    if (i.npc)
        units = Math.min(units, s.gold / (data_1.RESOURCE_META[r].price * (s.researched.includes('commerce') ? 1.05 : 1.15)));
    units = Math.max(0, units);
    i.inventory[r] -= units;
    ship.cargo[r] += units;
    if (i.npc)
        s.gold = Math.max(0, s.gold - units * data_1.RESOURCE_META[r].price * (s.researched.includes('commerce') ? 1.05 : 1.15));
}
function unloadCargo(s, ship, i) {
    let room = Math.max(0, getIslandStats(s, i.id).capacity - total(i.inventory)), delivered = 0;
    for (const r of types_1.RESOURCES) {
        const units = Math.min(ship.cargo[r], room);
        ship.cargo[r] -= units;
        i.inventory[r] += units;
        room -= units;
        delivered += units;
        if (i.npc)
            s.gold += units * data_1.RESOURCE_META[r].price * .85;
    }
    return delivered;
}
function createRoute(s, shipId, fromId, toId, resource, amount, returnResource = null) {
    const ship = s.ships.find(o => o.id === shipId), from = s.islands.find(i => i.id === fromId), to = s.islands.find(i => i.id === toId);
    if (!ship || !from || !to)
        return result(false, 'Choose a ship and two ports.');
    if (from === to)
        return result(false, 'Choose two different islands.');
    if (!from.discovered || !to.discovered || (!from.settled && !from.npc) || (!to.settled && !to.npc) || !active(from, 'harbor') || !active(to, 'harbor'))
        return result(false, 'Both islands need a discovered, inhabited harbor.');
    if (from.npc && to.npc)
        return result(false, 'At least one port must belong to your colony.');
    if (!types_1.RESOURCES.includes(resource) || (returnResource !== null && !types_1.RESOURCES.includes(returnResource)) || !Number.isInteger(amount) || amount < 1 || amount > ship.capacity)
        return result(false, `Cargo amount must be between 1 and ${ship.capacity}.`);
    try {
        routePath(s, from, to);
    }
    catch {
        return result(false, 'No safe sea route between these harbors.');
    }
    // Editing a route retains its ship cargo; no goods are duplicated or silently discarded.
    const trips = s.routes.filter(r => r.shipId === shipId).reduce((n, r) => n + r.trips, 0);
    s.routes = s.routes.filter(r => r.shipId !== shipId);
    const route = { id: id(s, 'route'), shipId, from: fromId, to: toId, resource, amount, returnResource, leg: 'outbound', progress: 0, active: true, trips };
    s.routes.push(route);
    ship.routeId = route.id;
    Object.assign(ship, port(from));
    unloadCargo(s, ship, from);
    loadCargo(s, ship, from, resource, amount);
    ship.status = `Sailing to ${to.name}`;
    note(s, `${ship.name}: ${from.name} ↔ ${to.name}.`, 'good');
    return result(true, 'Automated route established.');
}
function productionFactor(s, i, type) {
    let f = 1;
    if ((type === 'lumberyard' || type === 'teahouse') && i.biome === 'tropical')
        f *= 1.3;
    if ((type === 'quarry' || type === 'ironmine') && i.biome === 'volcanic')
        f *= 1.35;
    if ((type === 'farm' || type === 'fishery') && s.researched.includes('agriculture'))
        f *= 1.25;
    if (type === 'farm' && s.events.some(e => e.type === 'drought'))
        f *= .4;
    if (type === 'fishery' && s.events.some(e => e.type === 'storm') && !active(i, 'lighthouse'))
        f *= .35;
    return f;
}
function step(s, dt) {
    s.time += dt;
    for (const i of s.islands) {
        if (i.npc) {
            for (const r of types_1.RESOURCES)
                i.inventory[r] = Math.min(350, i.inventory[r] + dt * .04);
            continue;
        }
        if (!i.settled)
            continue;
        const stats = getIslandStats(s, i.id);
        const demand = i.buildings.filter(b => b.enabled).reduce((n, b) => n + data_1.BUILDINGS[b.type].workers, 0);
        const labor = demand ? Math.min(1, stats.workers / demand) : 1;
        for (const b of i.buildings) {
            const d = data_1.BUILDINGS[b.type];
            if (!b.enabled) {
                b.status = 'Paused';
                continue;
            }
            if (!d.output) {
                b.status = d.workers && labor < 1 ? 'Short of workers' : 'Operating';
                continue;
            }
            if (labor === 0) {
                b.status = 'Needs workers';
                continue;
            }
            if (d.input && !has(i.inventory, d.input)) {
                b.status = `Needs ${types_1.RESOURCES.filter(r => i.inventory[r] < (d.input?.[r] ?? 0)).map(r => data_1.RESOURCE_META[r].name).join(', ')}`;
                continue;
            }
            const net = sum(d.output) - sum(d.input ?? {});
            if (total(i.inventory) + net > stats.capacity + 1e-8) {
                b.status = 'Storage full';
                continue;
            }
            b.progress += dt / d.duration * labor * productionFactor(s, i, b.type);
            b.status = labor < .99 ? 'Short of workers' : 'Producing';
            while (b.progress >= 1 - 1e-9) {
                if ((d.input && !has(i.inventory, d.input)) || total(i.inventory) + net > stats.capacity + 1e-8) {
                    b.progress = Math.min(b.progress, 1);
                    break;
                }
                pay(i.inventory, d.input ?? {});
                for (const r of types_1.RESOURCES)
                    i.inventory[r] += d.output[r] ?? 0;
                b.progress = Math.max(0, b.progress - 1);
            }
        }
        let food = stats.population * .007 * dt;
        const fish = Math.min(food, i.inventory.fish);
        i.inventory.fish -= fish;
        food -= fish;
        i.inventory.grain = Math.max(0, i.inventory.grain - food);
        i.inventory.cloth = Math.max(0, i.inventory.cloth - stats.population * .00035 * dt);
        i.inventory.tea = Math.max(0, i.inventory.tea - stats.population * .0005 * dt);
        s.gold += stats.population * .007 * stats.happiness / 100 * (active(i, 'market') ? 1.2 : 1) * dt;
        s.knowledge += (.025 + active(i, 'school') * .14 * labor) * dt;
    }
    for (const r of s.routes) {
        const ship = s.ships.find(p => p.id === r.shipId);
        if (!r.active) {
            ship.status = 'Route paused';
            continue;
        }
        const from = s.islands.find(i => i.id === (r.leg === 'outbound' ? r.from : r.to)), to = s.islands.find(i => i.id === (r.leg === 'outbound' ? r.to : r.from));
        if (!active(from, 'harbor') || !active(to, 'harbor')) {
            ship.status = 'Waiting: a route harbor is paused';
            continue;
        }
        const path = routePath(s, from, to);
        const lens = path.slice(1).map((p, n) => Math.hypot(p.x - path[n].x, p.z - path[n].z));
        const length = lens.reduce((a, b) => a + b, 0);
        const storm = s.events.some(e => e.type === 'storm') ? .55 : 1;
        const lighthouse = s.islands.some(i => i.settled && active(i, 'lighthouse')) ? 1.15 : 1;
        const speed = 1.25 * storm * lighthouse * (s.researched.includes('navigation') ? 1.2 : 1);
        r.progress = Math.min(1, r.progress + dt * speed / length);
        let distance = r.progress * length;
        for (let n = 0; n < lens.length; n++) {
            if (distance <= lens[n] || n === lens.length - 1) {
                const t = Math.min(1, distance / lens[n]);
                ship.x = path[n].x + (path[n + 1].x - path[n].x) * t;
                ship.z = path[n].z + (path[n + 1].z - path[n].z) * t;
                break;
            }
            distance -= lens[n];
        }
        ship.status = `Sailing to ${to.name}`;
        if (r.progress >= 1) {
            const delivered = unloadCargo(s, ship, to);
            if (delivered > 0)
                r.trips++;
            r.leg = r.leg === 'outbound' ? 'return' : 'outbound';
            r.progress = 0;
            loadCargo(s, ship, to, r.leg === 'return' ? r.returnResource : r.resource, r.amount);
            ship.status = total(ship.cargo) >= ship.capacity - .01 ? 'Cargo hold full' : `Departing ${to.name}`;
        }
    }
    for (const e of s.events)
        e.remaining -= dt;
    s.events = s.events.filter(e => e.remaining > 0);
    if (s.time >= s.nextEvent) {
        const rng = random(`${s.seed}:event:${s.nextEvent}`);
        const type = ['storm', 'festival', 'drought', 'windfall'][Math.floor(rng() * 4)];
        const details = { storm: ['Storm front', 'Rough seas slow ships and unprotected fisheries.'], festival: ['Founders’ festival', 'Celebrations raise settlement happiness.'], drought: ['Dry season', 'Grain harvests slow until the rains return.'], windfall: ['Driftwood bounty', 'Salvagers recover timber for your home island.'] }[type];
        const event = { id: id(s, 'event'), type, title: details[0], description: details[1], remaining: type === 'windfall' ? 30 : 60 + rng() * 45 };
        s.events.push(event);
        if (type === 'windfall') {
            const h = s.islands[0];
            h.inventory.wood += Math.max(0, Math.min(30, getIslandStats(s, h.id).capacity - total(h.inventory)));
        }
        note(s, `${event.title}: ${event.description}`, type === 'storm' || type === 'drought' ? 'warning' : 'good');
        s.nextEvent += 240 + Math.floor(rng() * 100);
    }
    if (!s.victory && getObjectives(s).every(o => o.complete)) {
        s.victory = true;
        note(s, 'The islands are united! Your maritime republic enters a new age. Continue building in sandbox mode.', 'good');
    }
}
function tick(s, dt) { if (!Number.isFinite(dt) || dt <= 0)
    return; let remaining = Math.min(dt, 86400); while (remaining > 1e-8) {
    const d = Math.min(.5, remaining);
    step(s, d);
    remaining -= d;
} }
function getObjectives(s) {
    const colonies = s.islands.filter(i => i.settled && !i.npc);
    return [
        { id: 'settlements', title: 'An island union', description: 'Establish three island settlements.', current: colonies.length, target: 3, complete: colonies.length >= 3 },
        { id: 'population', title: 'A thriving people', description: 'Provide homes for 72 settlers across your islands.', current: colonies.reduce((n, i) => n + getIslandStats(s, i.id).population, 0), target: 72, complete: colonies.reduce((n, i) => n + getIslandStats(s, i.id).population, 0) >= 72 },
        { id: 'research', title: 'An age of discovery', description: 'Complete all twelve technologies.', current: s.researched.length, target: 12, complete: s.researched.length >= 12 },
        { id: 'trade', title: 'Connected shores', description: 'Complete 20 automated cargo deliveries.', current: s.routes.reduce((n, r) => n + r.trips, 0), target: 20, complete: s.routes.reduce((n, r) => n + r.trips, 0) >= 20 },
        { id: 'monument', title: 'A lasting legacy', description: 'Build a Union Monument.', current: colonies.reduce((n, i) => n + active(i, 'monument'), 0), target: 1, complete: colonies.some(i => active(i, 'monument') > 0) },
    ];
}
function serializeGame(s) { return JSON.stringify(s); }
function parseSave(raw) {
    if (typeof raw !== 'string' || raw.length > 5_000_000)
        throw new Error('Save file is too large.');
    let v;
    try {
        v = JSON.parse(raw);
    }
    catch {
        throw new Error('This file is not valid JSON.');
    }
    const fail = () => { throw new Error('Invalid or incompatible Tidebound save.'); };
    const obj = (x) => x !== null && typeof x === 'object' && !Array.isArray(x);
    const num = (x, min = 0, max = 1e12) => typeof x === 'number' && Number.isFinite(x) && x >= min && x <= max;
    const str = (x, max = 200) => typeof x === 'string' && x.length > 0 && x.length <= max;
    const arr = (x, max) => Array.isArray(x) && x.length <= max;
    const inv = (x) => obj(x) && types_1.RESOURCES.every(r => num(x[r]));
    const bool = (x) => typeof x === 'boolean';
    if (!obj(v) || v.version !== 1 || !str(v.seed) || !num(v.time) || !num(v.gold) || !num(v.knowledge) || ![0, 1, 2, 4].includes(v.speed) || !num(v.nextId, 1) || !Number.isInteger(v.nextId) || !num(v.nextEvent) || !bool(v.victory) || !num(v.tutorialStep, 0, 100) || !arr(v.islands, 30) || v.islands.length < 1 || !arr(v.ships, 200) || !arr(v.routes, 200) || !arr(v.researched, data_1.TECHNOLOGIES.length) || !arr(v.events, 20) || !arr(v.log, 100) || !obj(v.settings))
        fail();
    if (!num(v.settings.music, 0, 1) || !num(v.settings.effects, 0, 1) || !bool(v.settings.reducedMotion) || !bool(v.settings.shadows))
        fail();
    const allIds = new Set();
    const unique = (x) => { if (!str(x) || !/^(island|building|ship|route|event)-\d+$/.test(x) || !Number.isSafeInteger(Number(x.split('-')[1])) || allIds.has(x))
        fail(); allIds.add(x); };
    for (const i of v.islands) {
        if (!obj(i) || !str(i.name) || !['temperate', 'tropical', 'volcanic'].includes(i.biome) || !num(i.x, -1000, 1000) || !num(i.z, -1000, 1000) || !num(i.radius, 3, 100) || !bool(i.discovered) || !bool(i.settled) || !bool(i.npc) || !inv(i.inventory) || !arr(i.tiles, 2000) || !i.tiles.length || !arr(i.buildings, 2000))
            fail();
        unique(i.id);
        const tiles = new Set();
        for (const t of i.tiles) {
            if (!obj(t) || !Number.isInteger(t.x) || !Number.isInteger(t.z) || !num(t.x, -50, 50) || !num(t.z, -50, 50) || !num(t.height, 0, 20) || !['grass', 'sand', 'rock'].includes(t.kind))
                fail();
            const k = `${t.x},${t.z}`;
            if (tiles.has(k))
                fail();
            tiles.add(k);
        }
        const occupied = new Set();
        for (const b of i.buildings) {
            if (!obj(b) || !Object.hasOwn(data_1.BUILDINGS, b.type) || !tiles.has(`${b.x},${b.z}`) || occupied.has(`${b.x},${b.z}`) || !bool(b.enabled) || !num(b.progress, 0, 100) || !str(b.status))
                fail();
            occupied.add(`${b.x},${b.z}`);
            unique(b.id);
        }
    }
    const islandIds = new Set(v.islands.map((i) => i.id));
    if (!v.islands.some((i) => i.settled && !i.npc) || v.nextEvent < v.time)
        fail();
    const home = v.islands[0];
    if (home.id !== 'island-0' || !home.settled || home.npc || !home.discovered || !home.buildings.some((b) => b.type === 'harbor' && coastal(home, b.x, b.z)))
        fail();
    for (let a = 0; a < v.islands.length; a++) {
        const i = v.islands[a];
        if (i.npc && i.settled || i.settled && !i.discovered)
            fail();
        for (let b = a + 1; b < v.islands.length; b++) {
            const j = v.islands[b];
            if (Math.hypot(i.x - j.x, i.z - j.z) < i.radius + j.radius + 2)
                fail();
        }
    }
    for (const ship of v.ships) {
        if (!obj(ship) || !str(ship.name) || !islandIds.has(ship.home) || !num(ship.x, -2000, 2000) || !num(ship.z, -2000, 2000) || !inv(ship.cargo) || !num(ship.capacity, 1, 10000) || total(ship.cargo) > ship.capacity + 1e-6 || (ship.routeId !== null && !str(ship.routeId)) || !str(ship.status))
            fail();
        unique(ship.id);
    }
    const shipIds = new Set(v.ships.map((ship) => ship.id));
    const routedShips = new Set();
    for (const r of v.routes) {
        if (!obj(r) || !shipIds.has(r.shipId) || routedShips.has(r.shipId) || !islandIds.has(r.from) || !islandIds.has(r.to) || r.from === r.to || !types_1.RESOURCES.includes(r.resource) || !(r.returnResource === null || types_1.RESOURCES.includes(r.returnResource)) || !num(r.amount, 1, 10000) || !Number.isInteger(r.amount) || !['outbound', 'return'].includes(r.leg) || !num(r.progress, 0, 1) || !bool(r.active) || !num(r.trips) || !Number.isInteger(r.trips))
            fail();
        unique(r.id);
        routedShips.add(r.shipId);
        const ship = v.ships.find((p) => p.id === r.shipId);
        if (ship.routeId !== r.id || r.amount > ship.capacity)
            fail();
        for (const key of ['from', 'to']) {
            const i = v.islands.find((i) => i.id === r[key]);
            if (!i.discovered || (!i.settled && !i.npc) || !i.buildings.some((b) => b.type === 'harbor'))
                fail();
        }
    }
    for (const ship of v.ships)
        if (ship.routeId !== null && !v.routes.some((r) => r.id === ship.routeId && r.shipId === ship.id))
            fail();
    if (new Set(v.researched).size !== v.researched.length || v.researched.some((r) => !data_1.TECHNOLOGIES.some(t => t.id === r)))
        fail();
    for (const r of v.researched) {
        const t = data_1.TECHNOLOGIES.find(t => t.id === r);
        if (t.requires.some(req => !v.researched.includes(req)))
            fail();
    }
    for (const e of v.events) {
        if (!obj(e) || !['storm', 'festival', 'drought', 'windfall'].includes(e.type) || !str(e.title) || !str(e.description, 1000) || !num(e.remaining, 0, 10000))
            fail();
        unique(e.id);
    }
    for (const l of v.log)
        if (!obj(l) || !num(l.id) || l.id >= v.nextId || !num(l.time, 0, v.time) || !str(l.text, 2000) || !['info', 'good', 'warning'].includes(l.tone))
            fail();
    for (const i of v.islands)
        if (!i.id.startsWith('island-') || i.buildings.some((b) => !b.id.startsWith('building-')))
            fail();
    if (v.ships.some((ship) => !ship.id.startsWith('ship-')) || v.routes.some((r) => !r.id.startsWith('route-')) || v.events.some((e) => !e.id.startsWith('event-')))
        fail();
    // Island IDs are world indices; all other IDs share the nextId allocator.
    for (const key of allIds) {
        if (!key.startsWith('island-')) {
            const suffix = Number(key.split('-').at(-1));
            if (!Number.isInteger(suffix) || suffix >= v.nextId)
                fail();
        }
    }
    try {
        for (const r of v.routes)
            routePath(v, v.islands.find((i) => i.id === r.from), v.islands.find((i) => i.id === r.to));
    }
    catch {
        fail();
    }
    return v;
}
