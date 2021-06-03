################################################################################################################################
# This function implements the image search/retrieval .
# inputs: Input location of uploaded image, extracted vectors
#
################################################################################################################################
import os
import pickle
import numpy as np
from pathlib import Path
import tensorflow.compat.v1 as tf
from scipy.spatial.distance import cosine
from tensorflow.python.platform import gfile

BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
BOTTLENECK_TENSOR_SIZE = 2048
MODEL_INPUT_WIDTH = 299
MODEL_INPUT_HEIGHT = 299
MODEL_INPUT_DEPTH = 3
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'
RESIZED_INPUT_TENSOR_NAME = 'ResizeBilinear:0'
MAX_NUM_IMAGES_PER_CLASS = 2 ** 27 - 1  # ~134M

result_path = Path('static/result')
result_path.mkdir(exist_ok=True)

with open('neighbor_list_recom.pickle', 'rb') as f:
    neighbor_list = pickle.load(f)

#show_neighbors(random.randint(0, len(extracted_features)), indices, neighbor_list)


def get_top_k_similar(image_data, pred, pred_final, k):
    print("total data", len(pred))
    print(image_data.shape)

    top_k_ind = np.argsort([cosine(image_data, pred_row) for pred_row in pred])[:k]
    return [Path(pred_final[neighbor]).name[2:-4] for neighbor in top_k_ind]


def create_inception_graph():
    """"Creates a graph from saved GraphDef file and returns a Graph object.

    Returns:
      Graph holding the trained Inception network, and various tensors we'll be
      manipulating.
    """
    with tf.Session() as sess:
        model_filename = os.path.join('imagenet', 'classify_image_graph_def.pb')
        with gfile.GFile(model_filename, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            bottleneck_tensor, jpeg_data_tensor, resized_input_tensor = (
                tf.import_graph_def(graph_def, name='', return_elements=[
                    BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME,
                    RESIZED_INPUT_TENSOR_NAME]))
    return sess.graph, bottleneck_tensor, jpeg_data_tensor, resized_input_tensor


def run_bottleneck_on_image(sess, image_data, image_data_tensor, bottleneck_tensor):
    bottleneck_values = sess.run(bottleneck_tensor, {image_data_tensor: image_data})
    bottleneck_values = np.squeeze(bottleneck_values)
    return bottleneck_values


def recommend(image_data, extracted_features, k=9):
    tf.reset_default_graph()
    config = tf.ConfigProto(
        device_count={'GPU': 1}
    )
    sess = tf.Session(config=config)
    _, bottleneck_tensor, jpeg_data_tensor, _ = create_inception_graph()
    features = run_bottleneck_on_image(sess, image_data, jpeg_data_tensor, bottleneck_tensor)
    return get_top_k_similar(features, extracted_features, neighbor_list, k)
