
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier

# known words
known = {
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
    'cerezo': 'Material', 'marinas': 'Material', 'blanco': 'Color', 'rosa': 'Color', 'rojo': 'Color',
    'transparente': 'Color', 'naranja': 'Color', 'beige': 'Color', 'amarillo': 'Color', 'azul': 'Color',
    'negro': 'Color', 'cobre': 'Color', 'turquesa': 'Color', 'dorado': 'Color', 'verde': 'Color',
    'gris': 'Color', 'mostaza': 'Color', 'lila': 'Color', 'multicolor': 'Color', 'plateado': 'Color',
    'natural': 'Color', 'marrón': 'Color', 'recibidor': 'Habitación', 'trabajo': 'Habitación',
    'comedor': 'Habitación', 'dormitorio': 'Habitación', 'cocina': 'Habitación', 'salón': 'Habitación',
    'baño': 'Habitación', 'terraza': 'Habitación'
}

def load_knn(path):
    # "finalized_model.sav"
    return pickle.load(open(path, 'rb'))

def get_attr_cat(word, model, knn, known):
    """
    Given a word or list of words, returns a classification btwn
    ["Material", "Color", "Habitación", "not_an_attr_cat"]  according to either an
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