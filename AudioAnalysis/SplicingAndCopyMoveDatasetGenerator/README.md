# Splicing and Copy-Move Dataset Generator #

Este código consiste en 2 generadores de conjuntos de datos diferentes que utilizan el conjunto de datos TIMIT y aplican copy-move y splicing a cada audio.

El código funciona de la siguiente manera:

- PRIMER MÉTODO - RandomPosition:
    Para cada audio se extrae un segmento aleatorio de ese audio y se selecciona un punto aleatorio para insertar el segmento en ese punto, luego inserta el resto del audio original después del segmento modificado.

- SEGUNDO MÉTODO - Concatenación (basado en el artículo «Autoencoder for foregery detection»):
    Para cada audio sustraemos segmentos de 2s y 1s y los concatenamos de diferentes maneras de forma que creamos para cada audio original audios forjados de 3s y 2s. Concatenamos segmentos de distintos audios o repetidos de un mismo audio para generar los audios modificados con copy-move y splicing.
