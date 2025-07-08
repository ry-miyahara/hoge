class Circle:
    def __init__(self,r,name,place):
        self.r=r
        self.name=name
        self.place=place
        self.__pi=3.14

    def length(self):
        print(self.name)
        return self.r*2*self.__pi

    def area(self):
        print(self.place)
        return self.r*self.r*self.__pi

if __name__ == '__main__':
    maru=Circle(5,"miyah","tokyo")
    maru.length()
    maru.area()
