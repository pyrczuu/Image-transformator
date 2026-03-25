from data_augmentation import dataAugmentation


def main():
    dataAugmentation(class_dir="images/classes", background_dir="images/backgrounds", goal=150, log_path=None)

if __name__ == "__main__":
    main()