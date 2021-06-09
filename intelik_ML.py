import os
import zipfile
print(os.getcwd())


potato_dir = os.path.join('/Users/Center_Research/Documents/INTELIK/tmp/train/potato')
hamburger_dir = os.path.join('/Users/Center_Research/Documents/INTELIK/tmp/train/hamburger')
beer_dir = os.path.join('/Users/Center_Research/Documents/INTELIK/tmp/train/beer')
broccoli_dir = os.path.join('/Users/Center_Research/Documents/INTELIK/tmp/train/broccoli')
egg_dir = os.path.join('/Users/Center_Research/Documents/INTELIK/tmp/train/egg')
strawberry_dir = os.path.join('/Users/Center_Research/Documents/INTELIK/tmp/train/strawberry')
watermelon_dir = os.path.join('/Users/Center_Research/Documents/INTELIK/tmp/train/watermelon')
pasta_dir = os.path.join('/Users/Center_Research/Documents/INTELIK/tmp/train/pasta')
cabbage_dir = os.path.join('/Users/Center_Research/Documents/INTELIK/tmp/train/cabbage')

potato_files = os.listdir(potato_dir)
hamburger_files = os.listdir(hamburger_dir)
beer_files = os.listdir(beer_dir)
broccoli_files = os.listdir(broccoli_dir)
egg_files = os.listdir(egg_dir)
strawberry_files = os.listdir(strawberry_dir)
watermelon_files = os.listdir(watermelon_dir)
pasta_files = os.listdir(pasta_dir)
cabbage_files = os.listdir(cabbage_dir)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

pic_index = 2
next_potato = [os.path.join(potato_dir, fname)
                for fname in potato_files[pic_index-2:pic_index]]
next_hamburger = [os.path.join(hamburger_dir, fname)
                for fname in hamburger_files[pic_index-2:pic_index]]
next_beer = [os.path.join(beer_dir, fname)
                for fname in beer_files[pic_index-2:pic_index]]
next_broccoli = [os.path.join(broccoli_dir, fname)
                for fname in broccoli_files[pic_index-2:pic_index]]
next_egg = [os.path.join(egg_dir, fname)
                for fname in egg_files[pic_index-2:pic_index]]
next_strawberry = [os.path.join(strawberry_dir, fname)
                for fname in strawberry_files[pic_index-2:pic_index]]
next_watermelon = [os.path.join(watermelon_dir, fname)
                for fname in watermelon_files[pic_index-2:pic_index]]
next_pasta = [os.path.join(pasta_dir, fname)
                for fname in pasta_files[pic_index-2:pic_index]]
next_cabbage = [os.path.join(cabbage_dir, fname)
                for fname in cabbage_files[pic_index-2:pic_index]]

for i, img_path in enumerate(next_potato+next_hamburger+next_beer+next_broccoli+next_egg+next_strawberry+next_watermelon+next_pasta+next_cabbage):
  #print(img_path)
  # img = mpimg.imread(img_path)
  # plt.imshow(img)
  # plt.axis('Off')
  # plt.show()

###########################################################################################################
  import tensorflow as tf
  import keras_preprocessing
  from keras_preprocessing import image
  from keras_preprocessing.image import ImageDataGenerator

  TRAINING_DIR = "/Users/Center_Research/Documents/INTELIK/tmp/train"
  training_datagen = ImageDataGenerator(
      rescale=1. / 255,
      rotation_range=40,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest')  # Image Generator review

  VALIDATION_DIR = "/Users/Center_Research/Documents/INTELIK/tmp/validation"
  validation_datagen = ImageDataGenerator(rescale=1. / 255)

  train_generator = training_datagen.flow_from_directory(
      TRAINING_DIR,
      target_size=(150, 150),
      class_mode='categorical',
      batch_size=50
  )

  validation_generator = validation_datagen.flow_from_directory(
      VALIDATION_DIR,
      target_size=(150, 150),
      class_mode='categorical',
      batch_size=50
  )
  class myCallback(tf.keras.callbacks.Callback):
      def on_epoch_end(self, epoch, logs={}):
          if (logs.get('loss') < 0.4):
              print("\nReached 60% accuracy so cancelling training!")
              self.model.stop_training = True


  callbacks = myCallback()
###########################################################################################################
  model = tf.keras.models.Sequential([
      # Note the input shape is the desired size of the image 150x150 with 3 bytes color
      tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(150, 150, 3)),
      tf.keras.layers.MaxPooling2D(2, 2),
      tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
      tf.keras.layers.MaxPooling2D(2, 2),
      tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
      tf.keras.layers.MaxPooling2D(2, 2),
      tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
      tf.keras.layers.MaxPooling2D(2, 2),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dropout(0.5),
      tf.keras.layers.Dense(512, activation='relu'),
      tf.keras.layers.Dense(9, activation='softmax')
  ])

  model.summary()

  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

  history = model.fit(train_generator, epochs=200, steps_per_epoch=10, validation_data=validation_generator, verbose=1,
                      validation_steps=3, callbacks=[callbacks])

  # # evaluate the model
  # scores = model.evaluate()
  # print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

  # serialize model to JSON
  model_json = model.to_json()
  with open("model.h5", "w") as json_file:
      json_file.write(model_json)
  # serialize weights to HDF5
  model.save_weights("model.h5")
  print("Saved model to disk")

  # model.save("intelik.") #DATA MODEL SAVE
  # model = tf.keras.models.load_model('model.h5')
  converter = tf.lite.TFLiteConverter.from_keras_model(model)
  tflite_model = converter.convert()
  open("converted_model.tflite", "wb").write(tflite_model)
