from project import translate_text, get_response, synthesize_notes

def test_translate_text():
    assert translate_text('hello', 'it') == 'ciao'

def test_get_response():
    assert isinstance(get_response('Come si costruisce una macchina?'), str)

def test_synthesize_notes():
    assert isinstance(synthesize_notes("Il racconto fantastico nasce tra la fine del settecento e l’inizio dell’Ottocento con il Romanticismo tedesco, ma già a partire dal XVIII secolo aveva preso campo un genere narrativo che può essere considerato una delle prime manifestazioni del fantastico, il romanzo gotico. Il nome gotico gli viene attribuito perché in quel periodo avveniva la rinascita dello stile gotico in architettura e veniva riscoperto il Medioevo e il termine nero, dato che i fatti raccontati incutevano terrore e paura."), str)
