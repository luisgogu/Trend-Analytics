
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier

# known words
known = {
    # material
    'fraxinus': 'Material', 'radiata': 'Material', 'acero': 'Material', 'acrílicas': 'Material',
    'caoba': 'Material', 'polipropileno': 'Material', 'mays': 'Material', 'metal': 'Material',
    'templado': 'Material', 'felpa': 'Material', 'fimbristylis': 'Material', 'melia': 'Material',
    'pino': 'Material', 'triplochiton': 'Material', 'partículas': 'Material', 'abs': 'Material',
    'ulmus': 'Material', 'vaca': 'Material', 'pinaster': 'Material', 'maciza': 'Material',
    'eps': 'Material', 'samanea': 'Material', 'sintético': 'Material', 'hormigon': 'Material',
    'cuerda': 'Material', 'elastica': 'Material', 'textileno': 'Material', 'manufacturada': 'Material',
    'ratán': 'Material', 'arce': 'Material', 'cemento': 'Material', 'galvanizado': 'Material',
    'sintética': 'Material', 'regia': 'Material', 'aucoumea': 'Material', 'madera': 'Material',
    'tela': 'Material', 'tejer': 'Material', 'resina': 'Material', 'betula': 'Material',
    'latón': 'Material', 'costata': 'Material', 'terrazo': 'Material', 'nylon': 'Material',
    'papel': 'Material', 'piel': 'Material', 'lino': 'Material', 'yute': 'Material', 'nogal': 'Material',
    'teca': 'Material', 'cunninghamia': 'Material', 'viña': 'Material', 'globulosa': 'Material',
    'plástico': 'Material', 'poliestireno': 'Material', 'hierro': 'Material', 'piedra': 'Material',
    'aluminio': 'Material', 'policloruro': 'Material', 'fresno': 'Material', 'tejido': 'Material',
    'caña': 'Material', 'saman': 'Material', 'polietileno': 'Material', 'tapizado': 'Material',
    'naturales': 'Material', 'recicladas': 'Material', 'spp.': 'Material', 'espuma': 'Material',
    'algodón': 'Material', 'media': 'Material', 'albizia': 'Material', 'lato': 'Material',
    'poliuretano': 'Material', 'vinilo': 'Material', 'azedarach': 'Material', 'tectona': 'Material',
    'acacia': 'Material', 'rafia': 'Material', 'contrachapado': 'Material', 'búfalo': 'Material',
    'hevea': 'Material', 'cerámico': 'Material', 'mangium': 'Material', 'tablero': 'Material',
    'lana': 'Material', 'haya': 'Material', 'mármol': 'Material', 'zea': 'Material', 'roble':'Material'
    , 'cabra': 'Material', 'melamina': 'Material', 'alba': 'Material', 'poliéster': 'Material',
    'cerezo': 'Material', 'marinas': 'Material',
    # color
    'blanco': 'Color', 'rosa': 'Color', 'rojo': 'Color',
    'transparente': 'Color', 'naranja': 'Color', 'beige': 'Color', 'amarillo': 'Color', 'azul': 'Color',
    'negro': 'Color', 'cobre': 'Color', 'turquesa': 'Color', 'dorado': 'Color', 'verde': 'Color',
    'gris': 'Color', 'mostaza': 'Color', 'lila': 'Color', 'multicolor': 'Color', 'plateado': 'Color',
    'natural': 'Color', 'marrón': 'Color',
    # habitacion
    'recibidor': 'Habitación', 'trabajo': 'Habitación',
    'comedor': 'Habitación', 'dormitorio': 'Habitación', 'cocina': 'Habitación', 'salón': 'Habitación',
    'baño': 'Habitación', 'terraza': 'Habitación',
    # estilo
    'vintage': 'Estilo','ecléctico': 'Estilo',
    'oriental': 'Estilo','escandinavo': 'Estilo','industrial': 'Estilo','minimalista': 'Estilo',
    'romántico': 'Estilo','moderno': 'Estilo','bohemio': 'Estilo','rústico': 'Estilo',
    # forma
    'Circular': 'Forma', 'Ovalado': 'Forma', 'Forma libre': 'Forma', 'Cónico': 'Forma',
    'Triangular': 'Forma', 'Cilindrico': 'Forma', 'Cuadrado': 'Forma', 'Geométrico': 'Forma',
    'Ovalada': 'Forma', 'Imitación': 'Forma', 'Hexágono': 'Forma', 'Amorfo': 'Forma',
    'Rectangular': 'Forma', 'Cilindrica': 'Forma', 'Cuadrada': 'Forma',
    # muebles
    'nórdico': 'Estilo','náutico': 'Estilo','clásico': 'Estilo', 
    'sofás': 'Mueble','sofá': 'Mueble','mesa': 'Mueble','mesas': 'Mueble','silla': 'Mueble','sillas': 'Mueble',
    'sillón': 'Mueble','sillones': 'Mueble','cama': 'Mueble','camas': 'Mueble','alfombra': 'Mueble',
    'alfombras': 'Mueble','jarrón': 'Mueble','jarrones': 'Mueble','estantería': 'Mueble',
    'estanterías': 'Mueble','librería': 'Mueble','librerías': 'Mueble','escritorio': 'Mueble',
    'escritorios': 'Mueble','colchón': 'Mueble','colchones': 'Mueble','cómodas': 'Mueble',
    'cómoda': 'Mueble','otomanas': 'Mueble','otomana': 'Mueble','mueble': 'Mueble','muebles': 'Mueble',
    'biblioteca': 'Mueble','bibliotecas': 'Mueble','futón': 'Mueble','futones': 'Mueble','litera': 'Mueble',
    'literas': 'Mueble','mesita': 'Mueble','mesitas': 'Mueble','mesón': 'Mueble','mesones': 'Mueble',
    'taburete': 'Mueble','taburetes': 'Mueble','espejo': 'Mueble','espejos': 'Mueble','armario': 'Mueble',
    'armarios': 'Mueble','banco': 'Mueble','bancos': 'Mueble','organizador': 'Mueble','organizadores': 'Mueble',
    'perchero': 'Mueble','percheros': 'Mueble','tocador': 'Mueble','tocadores': 'Mueble','somier': 'Mueble',
    'somieres': 'Mueble','lámpara': 'Mueble','lámparas': 'Mueble','butaca': 'Mueble','butacas': 'Mueble',
    'cambiador': 'Mueble','cambiadores': 'Mueble','chaiselongue': 'Mueble','chaiselongues': 'Mueble',
    'cojín': 'Mueble','cojines': 'Mueble','cuadro': 'Mueble','cuadros': 'Mueble','jarra': 'Mueble',
    'jarras': 'Mueble','colgador': 'Mueble','colgadores': 'Mueble','asiento': 'Mueble','asientos': 'Mueble',
    'reloj': 'Mueble','relojes': 'Mueble','toallero': 'Mueble','toalleros': 'Mueble','maceta': 'Mueble'
    ,'macetas': 'Mueble','tumbona': 'Mueble','tumbonas': 'Mueble','papel': 'Mueble','papeles': 'Mueble',
    'cesto': 'Mueble','cestos': 'Mueble','cesta': 'Mueble','cestas': 'Mueble','cuna': 'Mueble','cunas': 'Mueble',
    'trona': 'Mueble','tronas': 'Mueble','biombo': 'Mueble','biombos': 'Mueble','sofas': 'Mueble','sofa': 'Mueble',
    'couch': 'Mueble','chairs': 'Mueble','armchair': 'Mueble','armchairs': 'Mueble','rug': 'Mueble','carpets': 'Mueble',
    'vase': 'Mueble','vases': 'Mueble','shelving': 'Mueble','shelves': 'Mueble','bookstore': 'Mueble',
    'libraries': 'Mueble','desk': 'Mueble','desks': 'Mueble','mattress': 'Mueble','mattresses': 'Mueble',
    'piece of furniture': 'Mueble','furniture': 'Mueble','library': 'Mueble','run': 'Mueble','letter': 'Mueble',
    'small table': 'Mueble','table': 'Mueble','meson': 'Mueble','mesons': 'Mueble','stool': 'Mueble',
    'stools': 'Mueble','mirror': 'Mueble','mirrors': 'Mueble','closet': 'Mueble','wardrove': 'Mueble',
    'banks': 'Mueble','organizer': 'Mueble','organizers': 'Mueble','coat rack': 'Mueble','coat hangers': 'Mueble',
    'dresser': 'Mueble','players': 'Mueble','lamp': 'Mueble','lamps': 'Mueble','seat': 'Mueble','seats': 'Mueble',
    'changer': 'Mueble','changers': 'Mueble','cushion': 'Mueble','cushions': 'Mueble','picture': 'Mueble',
    'jug': 'Mueble','jugs': 'Mueble','hanger': 'Mueble','hangers': 'Mueble','seating': 'Mueble','watch': 'Mueble',
    'watches': 'Mueble','flowerpot': 'Mueble','pots': 'Mueble','deck chair': 'Mueble','loungers': 'Mueble',
    'paper': 'Mueble','papers': 'Mueble','dough': 'Mueble','baskets': 'Mueble','the road': 'Mueble','cradle': 'Mueble',
    'cribs': 'Mueble','trone': 'Mueble','screen': 'Mueble','biples': 'Mueble',
}

def load_knn(path):
    # "finalized_model.sav"
    return pickle.load(open(path, 'rb'))

def get_attr_cat(word, model, knn, known):
    """
    Given a word or list of words, returns a classification btwn
    ["Material", "Color", "Habitación","Estilo", "Forma", "not_an_attr_cat"]  according to either an
    existing dict (known) or a knn model (knn)

    Params:
        - word (str or list)
            Word(s) to be classified
        - model (gensim.models.keyedvectors.KeyedVectors)
            fastText language model
        - knn (sklearn.neighbors._classification.KNeighborsClassifier)
            Sklearn pretrained knn model
        - known (dict)
            Dict (k: word, v: attribute category)
    
    Returns
        - result (str or list)
    """    
    
    if isinstance(word, str):
        if word in known.keys():
            return known[word]
        if word in model:
            prediction = knn.predict(np.array([model[word]]))
            return prediction[0]
        return "not_an_attr"
    
    if isinstance(word, list):
        result = []
        for w in word:
            if w in known.keys():
                result.append(known[w])
            elif w in model:
                prediction = knn.predict(np.array([model[w]]))
                result.append(prediction[0])
            else:
                result.append("not_an_attr")
        return result
    
    else:
        raise TypeError("word should be str or list")
    
    return "No result returned"