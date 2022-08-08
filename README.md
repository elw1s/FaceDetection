# Face Detection using Insightface
Face Detection with age, gender and emotion attributes using pre-trained models (Onnx based)

#### gender_age.py

- Only detects face , gender and age. 
- No emotion detection
- RetinaFace-10GF	used (Single model)

#### gender_age_emotion.py

- Detects face, gender, age and emotion
- Fer+ dataset is used for emotion detection (https://github.com/microsoft/FERPlus)
- All pre-trained models are stored in folders (4 different models)
