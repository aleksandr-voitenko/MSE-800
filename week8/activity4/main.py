class UniversityConfig:
    _instance:UniversityConfig = None

    name: str = "";
    year: int = "";
    semester: int = "";

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance



def main():
    c1 = UniversityConfig()
    c1.name = "The best university"
    c1.year = 2050
    c1.semester = 1

    c2 = UniversityConfig()
    print(c2.name)
    print(c2.year)
    print(c2.semester)
    

if __name__ == "__main__":
    main()