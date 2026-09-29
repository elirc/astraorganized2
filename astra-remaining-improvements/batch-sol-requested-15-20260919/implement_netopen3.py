"""Apply the reviewed template ordering fix only after the immutable baseline exists."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from long_paths import extended_path

B=extended_path(Path(__file__).resolve().parent.parent)
assert (B/'baselines/b8fb41bd6255.json').is_file(), 'Wait for staging baseline before editing.'
P=B/'stage/b8fb41bd6255/Umbraco-CMS'
f=P/'src/Umbraco.Cms.Api.Management/Controllers/ManagementApiControllerBase.cs'
s=f.read_text(encoding='utf-8')
old='''        => entities.OrderBy(e => Array.IndexOf(requestedIds, e.Key)).ToList();'''
new='''    {
        var entitiesById = new Dictionary<Guid, TEntity>();
        foreach (TEntity entity in entities)
        {
            // The first hydrated entity wins if a service returns duplicates.
            entitiesById.TryAdd(entity.Key, entity);
        }

        var ordered = new List<TEntity>();
        foreach (Guid requestedId in requestedIds)
        {
            if (entitiesById.Remove(requestedId, out TEntity? entity))
            {
                ordered.Add(entity);
            }
        }

        return ordered;
    }'''
assert old in s
s=s.replace(old,new).replace('/// Orders entities to match the order of the requested IDs.',
    '/// Returns each requested entity once in requested-ID order, excluding missing and unrequested entities.')
f.write_text(s,encoding='utf-8')
f=P/'tests/Umbraco.Tests.UnitTests/Umbraco.Cms.Api.Management/Controllers/Template/Item/SearchTemplateItemControllerTests.cs'
s=f.read_text(encoding='utf-8');assert 'Search_Template_Item_Excludes_Unrequested' not in s
insert='''
    [Test]
    public async Task Search_Template_Item_Excludes_Unrequested_And_Missing_Entities_Without_Changing_Total()
    {
        var keyA = Guid.NewGuid();
        var missing = Guid.NewGuid();
        var keyB = Guid.NewGuid();
        var extra = Guid.NewGuid();
        SetSearchResult([keyA, missing, keyB], 19);
        _templateService.Setup(x => x.GetAllAsync(It.IsAny<Guid[]>())).ReturnsAsync(
            new[] { Template(keyB, "b"), Template(extra, "extra"), Template(keyA, "a") });

        PagedModel<TemplateItemResponseModel> result = await SearchResult();

        Assert.Multiple(() =>
        {
            Assert.That(result.Items.Select(x => x.Id), Is.EqualTo(new[] { keyA, keyB }));
            Assert.That(result.Total, Is.EqualTo(19));
        });
    }

    [Test]
    public async Task Search_Template_Item_Collapses_Duplicate_Keys_And_Keeps_First_Hydrated_Entity()
    {
        var keyA = Guid.NewGuid();
        var keyB = Guid.NewGuid();
        SetSearchResult([keyB, keyA, keyB, keyA], 4);
        _templateService.Setup(x => x.GetAllAsync(It.IsAny<Guid[]>())).ReturnsAsync(
            new[] { Template(keyA, "a-first"), Template(keyB, "b-first"), Template(keyB, "b-later"), Template(keyA, "a-later") });

        PagedModel<TemplateItemResponseModel> result = await SearchResult();

        Assert.Multiple(() =>
        {
            Assert.That(result.Items.Select(x => x.Id), Is.EqualTo(new[] { keyB, keyA }));
            Assert.That(result.Items.Select(x => x.Alias), Is.EqualTo(new[] { "b-first", "a-first" }));
            Assert.That(result.Total, Is.EqualTo(4));
        });
    }

    [Test]
    public async Task Search_Template_Item_Empty_Page_Preserves_Total_Without_Hydration_Or_Mapping()
    {
        SetSearchResult([], 17);

        PagedModel<TemplateItemResponseModel> result = await SearchResult();

        Assert.Multiple(() =>
        {
            Assert.That(result.Items, Is.Empty);
            Assert.That(result.Total, Is.EqualTo(17));
        });
        _templateService.Verify(x => x.GetAllAsync(It.IsAny<Guid[]>()), Times.Never);
        _mapper.Verify(x => x.MapEnumerable<ITemplate, TemplateItemResponseModel>(It.IsAny<IEnumerable<ITemplate>>()), Times.Never);
    }

    private void SetSearchResult(Guid[] keys, long total)
    {
        _entitySearchService
            .Setup(x => x.Search(UmbracoObjectTypes.Template, It.IsAny<string>(), It.IsAny<int>(), It.IsAny<int>()))
            .Returns(new PagedModel<IEntitySlim>
            {
                Items = keys.Select(key => (IEntitySlim)new EntitySlim { Key = key }).ToArray(),
                Total = total,
            });
        _mapper
            .Setup(x => x.MapEnumerable<ITemplate, TemplateItemResponseModel>(It.IsAny<IEnumerable<ITemplate>>()))
            .Returns<IEnumerable<ITemplate>>(entities =>
                entities.Select(entity => new TemplateItemResponseModel { Alias = entity.Alias, Id = entity.Key }).ToList());
    }

    private static ITemplate Template(Guid key, string alias) =>
        Mock.Of<ITemplate>(template => template.Key == key && template.Alias == alias);

    private async Task<PagedModel<TemplateItemResponseModel>> SearchResult()
    {
        IActionResult result = await _controller.Search(CancellationToken.None, "test");
        Assert.That(result, Is.TypeOf<OkObjectResult>());
        var value = ((OkObjectResult)result).Value;
        Assert.That(value, Is.TypeOf<PagedModel<TemplateItemResponseModel>>());
        return (PagedModel<TemplateItemResponseModel>)value!;
    }
'''
s=s.rstrip();assert s.endswith('}')
f.write_text(s[:-1]+insert+'}\n',encoding='utf-8')
print('Implemented requested-ID ordering and three controller regressions.')
