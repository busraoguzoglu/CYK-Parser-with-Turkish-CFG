from typing import List
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM, java

def main():
    ZEMBEREK_PATH = 'Zemberek/zemberek-full.jar'

    # Java virtual machine başlatmak gerekiyor, sıkıntılı.
    startJVM(getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))

    TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
    morphology = TurkishMorphology.createWithDefaults()

    kelimeler = 'kalem ilişkilendiremediklerimiz gözlük gözlem'
    analysis: java.util.ArrayList = (
        morphology.analyzeAndDisambiguate(kelimeler).bestAnalysis()
    )
    pos: List[str] = []
    for i, analysis in enumerate(analysis, start=1): f'\nAnalysis {i}: {analysis}',
    f'\nPrimary POS {i}: {analysis.getPos()}'
    f'\nPrimary POS (Short Form) {i}: {analysis.getPos().shortForm}'

    pos.append(
        f'{str(analysis.getLemmas()[0])}'
    )
    print(f'\n Kelime Kökleri: {" ".join(pos)}')

