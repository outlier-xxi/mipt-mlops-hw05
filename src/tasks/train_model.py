import os


def main():
    #config = Variable.get("ml_retrain_pipeline_config", deserialize_json=True)
    #model_version = config.get('MODEL_VERSION')
    model_version = os.getenv("MODEL_VERSION", "v1.0.0")
    
    # Place training code here
    
    
    print(f"Модель обучена: {model_version}")


if __name__ == "__main__":
    main()
