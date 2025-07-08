class Circle:
    __pi=3.14

    def length(self,r):
        return r*2*Circle.__pi

    def area(self,r):
        return r*r*Circle.__pi

if __name__ == '__main__':
    print(Circle().length(1))
    print(Circle().__pi)