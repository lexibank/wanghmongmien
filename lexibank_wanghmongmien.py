import attr
from pathlib import Path
from clldutils.misc import slug
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import Concept, Language
from pylexibank import progressbar


@attr.s
class CustomConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)
@attr.s
class CustomLanguage(Language):
    Family = attr.ib(default='Hmong-Mien')
    Source = attr.ib(default=None)

class Dataset(BaseDataset):
    id = 'wanghmongmien'
    dir = Path(__file__).parent
    concept_class = CustomConcept
    language_class = CustomLanguage
    

    def cmd_makecldf(self, args):

        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = '{0}_{1}'.format(concept.number, slug(concept.english))
            args.writer.add_concept(
                    ID=idx,
                    Name=concept.english,
                    Chinese_Gloss=concept.attributes['chinese'],
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss
                    )
            concepts[concept.attributes['chinese']+' '+concept.english] = idx
            concepts[concept.english] = idx
        args.writer.add_languages()
        args.writer.add_sources()

        for row, language in progressbar(zip(
                self.raw_dir.read_csv(
                    'data.tsv', 
                    delimiter='\t', 
                    dicts=True)[1:],
                self.languages)):
            for j, (concept, entry) in enumerate(list(row.items())[1:]):
                if entry.strip():
                    pidx = concepts.get(
                                concept, 
                                concepts.get(' '.join(concept.split(' ')[1:]), '?'))
                    args.writer.add_form(
                            Language_ID=language['ID'],
                            Parameter_ID=pidx,
                            Value=entry,
                            Form=entry.replace(" ", "_"),
                            Source=[language['Source']]
                            )
                



