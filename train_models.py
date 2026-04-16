from ml_models import train_and_save_models

if __name__ == '__main__':
    print('Training dummy ML models and saving to /models ...')
    lr, dt = train_and_save_models('models')
    print('Saved LR and DT models. Done!')
