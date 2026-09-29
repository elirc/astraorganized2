"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TECHNOLOGIES = exports.BUILDINGS = exports.RESOURCE_META = exports.TILE_SPACING = void 0;
exports.TILE_SPACING = 2;
exports.RESOURCE_META = {
    wood: { name: 'Timber', color: '#af8155', price: 3 }, stone: { name: 'Stone', color: '#aab8bf', price: 4 },
    fish: { name: 'Fish', color: '#70cfe6', price: 3 }, grain: { name: 'Grain', color: '#eac97a', price: 3 },
    planks: { name: 'Planks', color: '#d9a36b', price: 7 }, bricks: { name: 'Bricks', color: '#db8768', price: 8 },
    iron: { name: 'Iron', color: '#91a6ad', price: 9 }, tools: { name: 'Tools', color: '#bed1dc', price: 17 },
    cloth: { name: 'Cloth', color: '#c6a5e1', price: 10 }, tea: { name: 'Tea', color: '#8ac29b', price: 12 },
};
exports.BUILDINGS = {
    cottage: { id: 'cottage', name: 'Cottage', category: 'homes', description: 'Homes for 12 settlers. Each household contributes workers and tax income.', cost: { wood: 12, stone: 4 }, gold: 15, workers: 0, duration: 1, color: '#e9c59b' },
    lumberyard: { id: 'lumberyard', name: 'Lumberyard', category: 'production', description: 'Harvests renewable timber. Tropical forests grow faster.', cost: { wood: 8, stone: 2 }, gold: 12, workers: 3, duration: 9, output: { wood: 3 }, color: '#a77d56' },
    quarry: { id: 'quarry', name: 'Quarry', category: 'production', description: 'Extracts stone. Volcanic geology improves output.', cost: { wood: 12 }, gold: 20, workers: 3, duration: 11, output: { stone: 3 }, color: '#b3bec5' },
    fishery: { id: 'fishery', name: 'Fishery', category: 'production', description: 'Coastal fishing supplies food. Storms slow catches.', cost: { wood: 12, stone: 3 }, gold: 20, workers: 3, duration: 10, output: { fish: 4 }, coastal: true, color: '#64b6c8' },
    farm: { id: 'farm', name: 'Grain Farm', category: 'production', description: 'Grows grain for food and weaving. Drought reduces harvests.', cost: { wood: 16, stone: 4 }, gold: 25, workers: 4, duration: 15, output: { grain: 6 }, color: '#d7b56c' },
    warehouse: { id: 'warehouse', name: 'Warehouse', category: 'civic', description: 'Adds 600 units to this island’s shared storage capacity.', cost: { wood: 20, stone: 8 }, gold: 30, workers: 0, duration: 1, color: '#b88a60' },
    sawmill: { id: 'sawmill', name: 'Sawmill', category: 'production', description: 'Turns 3 timber into 2 construction planks.', cost: { wood: 24, stone: 12 }, gold: 35, workers: 4, duration: 12, input: { wood: 3 }, output: { planks: 2 }, unlock: 'forestry', color: '#c48e5c' },
    brickworks: { id: 'brickworks', name: 'Brickworks', category: 'production', description: 'Fires 3 stone into 2 bricks.', cost: { wood: 20, stone: 18 }, gold: 40, workers: 4, duration: 14, input: { stone: 3 }, output: { bricks: 2 }, unlock: 'masonry', color: '#ca7960' },
    ironmine: { id: 'ironmine', name: 'Iron Mine', category: 'production', description: 'Extracts iron ore, especially efficiently on volcanic islands.', cost: { planks: 12, stone: 22 }, gold: 55, workers: 5, duration: 15, output: { iron: 2 }, unlock: 'mining', color: '#778b94' },
    toolsmith: { id: 'toolsmith', name: 'Toolsmith', category: 'production', description: 'Forges 2 iron and 1 plank into 2 tools.', cost: { planks: 16, bricks: 12 }, gold: 65, workers: 5, duration: 18, input: { iron: 2, planks: 1 }, output: { tools: 2 }, unlock: 'metalworking', color: '#879ca9' },
    weaver: { id: 'weaver', name: 'Weaver', category: 'production', description: 'Weaves 3 grain into 2 cloth, fulfilling household needs.', cost: { planks: 12, stone: 10 }, gold: 45, workers: 4, duration: 16, input: { grain: 3 }, output: { cloth: 2 }, unlock: 'textiles', color: '#b297c7' },
    teahouse: { id: 'teahouse', name: 'Tea Garden', category: 'production', description: 'Produces tea for happier settlers. Tropical climate gives a bonus.', cost: { planks: 14, bricks: 8 }, gold: 50, workers: 4, duration: 18, output: { tea: 2 }, unlock: 'botany', color: '#79a887' },
    market: { id: 'market', name: 'Market Square', category: 'civic', description: 'Improves happiness and tax income through local exchange.', cost: { planks: 12, stone: 8 }, gold: 40, workers: 2, duration: 1, unlock: 'commerce', color: '#e4ae71' },
    school: { id: 'school', name: 'Academy', category: 'civic', description: 'Educated workers generate additional knowledge for research.', cost: { planks: 18, bricks: 12 }, gold: 65, workers: 3, duration: 1, unlock: 'education', color: '#b4c9d0' },
    shipyard: { id: 'shipyard', name: 'Shipyard', category: 'maritime', description: 'Build cargo ships from 20 planks, 8 cloth, and 90 gold.', cost: { planks: 25, stone: 20 }, gold: 85, workers: 0, duration: 1, coastal: true, unlock: 'shipbuilding', color: '#ac8263' },
    lighthouse: { id: 'lighthouse', name: 'Lighthouse', category: 'maritime', description: 'Improves fleet speed by 15% and protects this island from storms.', cost: { bricks: 25, tools: 8 }, gold: 90, workers: 0, duration: 1, coastal: true, unlock: 'navigation', color: '#eee0b9' },
    harbor: { id: 'harbor', name: 'Harbor', category: 'maritime', description: 'Connects your island to ships and international trade.', cost: { wood: 25, stone: 12 }, gold: 45, workers: 0, duration: 1, coastal: true, color: '#d9bb91' },
    monument: { id: 'monument', name: 'Union Monument', category: 'civic', description: 'The lasting symbol of a united archipelago. Required for victory.', cost: { planks: 70, bricks: 90, tools: 35, cloth: 25 }, gold: 450, workers: 0, duration: 1, unlock: 'architecture', color: '#f0d595' },
};
exports.TECHNOLOGIES = [
    { id: 'forestry', name: 'Sustainable Forestry', description: 'Unlock sawmills and construction planks.', cost: 18, requires: [] },
    { id: 'masonry', name: 'Masonry', description: 'Unlock brickworks and advanced construction.', cost: 22, requires: [] },
    { id: 'commerce', name: 'Island Markets', description: 'Unlock market squares and reduce trading fees.', cost: 28, requires: [] },
    { id: 'education', name: 'Public Education', description: 'Unlock academies for faster research.', cost: 30, requires: ['forestry', 'masonry'] },
    { id: 'textiles', name: 'Textile Craft', description: 'Unlock weavers and household cloth.', cost: 32, requires: ['forestry'] },
    { id: 'shipbuilding', name: 'Shipbuilding', description: 'Unlock shipyards and additional cargo ships.', cost: 38, requires: ['forestry', 'textiles'] },
    { id: 'mining', name: 'Deep Mining', description: 'Unlock iron mines.', cost: 38, requires: ['masonry'] },
    { id: 'metalworking', name: 'Metalworking', description: 'Unlock toolsmiths.', cost: 45, requires: ['mining'] },
    { id: 'botany', name: 'Tropical Botany', description: 'Unlock tea gardens.', cost: 40, requires: ['commerce'] },
    { id: 'navigation', name: 'Celestial Navigation', description: 'Found new island settlements, unlock lighthouses, and improve ship speed.', cost: 55, requires: ['shipbuilding'] },
    { id: 'agriculture', name: 'Crop Rotation', description: 'Farms and fisheries produce 25% faster.', cost: 48, requires: ['education', 'botany'] },
    { id: 'architecture', name: 'Grand Architecture', description: 'Unlock the Union Monument and a lasting legacy.', cost: 80, requires: ['metalworking', 'education', 'navigation'] },
];
