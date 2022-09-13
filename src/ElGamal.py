from math import gcd, sqrt
from hashlib import sha256
import random as rd

class ElGamal:

    def __init__(self):
        self.hashed = ""
        self.p = -1
        self.a = -1
        self.alpha = -1
        self.beta = -1
        self.key = -1
        self.sign1 = 0
        self.sign2 = []

    def isPrime(self, num):
        
        if num < 2:
            return False
        for i in range(2, int(sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True

    def enterP(self):
        num = 0
        while(self.isPrime(num) == False):

            try:
                num = int(input("Enter prime number: "))
            except ValueError:
                print ("Invalid Input")
        self.p = num

    def powmod(self, num, n, m):
        ans = []
        r = -1
        while(n!= 0):
            r = n % 2
            n = n // 2
            ans.insert(0,r)

        p = 1

        for ele in ans:
            p = p * p
            p = p % m
            if(ele == 1):
                p = p*num
                p = p % m
        return p

    def anvmod(self, a, n):
        
        s1, s2, t1, t2 = 1, 0, 0, 1
        r = -1
        q = 0
        save_n = n
        while(n%a != 0):

            q = n // a
            r = n % a

            s2, s1 = s1 - s2 * q, s2
            t2, t1 = t1 - t2 * q, t2
            n, a = a, r
        return t2 % save_n

    def autoFillP(self):

        minPrime = 100
        maxPrime = 1000000
        cached_primes = [i for i in range(minPrime,maxPrime) if self.isPrime(i)]

        self.p = int(rd.choice(cached_primes))

    def autoFillAlpha(self):
        self.alpha = rd.randint(1, self.p-2)

    def autoFillA(self):
        self.a = rd.randint(1, self.p-2)

    def autoFillBeta1(self):
        self.beta = (self.alpha**self.a) % self.p

    def autoFillBeta(self):
        
        self.beta = self.powmod(self.alpha, self.a, self.p)

    def getParameter(self):
        return self.p, self.alpha

    def getPubKey(self):
        return self.beta

    def getPriKey(self):
        return self.a

    def getPriK(self):
        return self.key

    def setHashed(self, message):
        self.hashed = sha256(message.encode("UTF-8")).hexdigest()

    def setP(self, p):
        self.p = p

    def setAlpha(self, alpha):
        self.alpha = alpha

    def setBeta(self, beta):
        self.beta = beta

    def setSign1(self, num):
        self.sign1 = num

    def setSign2(self, listNum):
        self.sign2 = listNum

    def findRandomPrivateKey(self):
        while 1:
            self.key = rd.randint(1,self.p-2)
            if gcd(self.key, self.p-1)==1: 
                break

    def display(self):
        print ("Public key: ", self.p, self.alpha, self.beta)
        print ("Private key: ", self.a)

    def SignatureGeneration(self):

        self.sign1 = self.powmod(self.alpha, self.key, self.p)

        anvKey = self.anvmod(self.key, self.p-1)
        self.sign2 = [(anvKey*((ord(char) - self.a*self.sign1)%(self.p-1)))%(self.p-1) for char in self.hashed]


    def getDigitalSignature(self):

        digitalSignature = chr(self.sign1)
        for num in self.sign2:
            digitalSignature += chr(num)
        return digitalSignature

    def setDigitalSignature(self, digitalSignature):

        self.sign1 = ord(digitalSignature[0])
        self.sign2 = []
        for index in range(1,len(digitalSignature)):
            self.sign2.append(ord(digitalSignature[index]))

    def SignatureVerification(self, message):
        if self.sign1 < 1 or self.sign1 > self.p-1:
            return False
        v1 = [self.powmod(self.beta,self.sign1,self.p)%self.p * self.powmod(self.sign1,num,self.p)%self.p for num in self.sign2]
            
        hashed2 = sha256(message.encode("UTF-8")).hexdigest()
        v2 = [self.powmod(self.alpha,ord(char),self.p) for char in hashed2]


        return v1==v2
        

# ord >< chr