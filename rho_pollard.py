"""
Copyright (c) 2021 Nathan Stchepinsky

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
    Proofs, explanations and pseudo-code can be found here (in french) : https://devnathan.github.io/source/TIPE.pdf
"""
import random
import sys
import string
import numpy as np
import hashlib



class Rho_pollard:
    """
        Arguments
        - Hash function attacked
        - Maximum length of the initial word, randomly generated
        - Optional argument. If true, all hashs generated are printed. Else (by default) only the number of hashs generated is printed.
    """
    def __init__(self,hash_func, len_max_word, is_printing_hash = False):
        self.len_max_word = len_max_word
        self.is_printing_hash = is_printing_hash
        self.hash_func = hash_func 

    def message_generator(self):
        '''
        PRIVATE FUNCTION
        Generate a random messages with a maximum length of max_length
        '''
        word_len = random.randint(1,self.len_max_word)
        message = ''.join([random.choice(string.ascii_letters + string.digits) for y in range(word_len)])   
        return message


    def H(self,hash):
        '''
        H function.
        '''
        return self.hash_func(hash)

    def R(self,hash):
        '''
        PRIVATE FUNCTION
        R function. Identity
        '''
        return hash

    def f(self,hash) :
        '''
        PRIVATE FUNCTION
        f function. f(x) = H(R(x))
        '''
        return self.H(self.R(hash))



    def search_j0(self,h0):
        '''
            PRIVATE FUNCTION
            Find the first value of j_0, ie when h_i = h'_i (h is a sequence defined by : for all i, h_i = f(h_(i-1). See the paper for more info.)
        '''
        print("[*] STEP 1 ...")
        h = self.f(h0)
        h_prime = self.f(self.f(h0))
        if self.is_printing_hash:
            print("hash1 =", h)
            print("hash2 = ", h_prime)
        j = 1
        old_h = [h,h]
        old_h_prime = [h_prime, h_prime]

        while h != h_prime :
            h = self.f(h)
            h_prime = self.f(self.f(h_prime))
            j+=1
            if j%100000 == 0:
                print(j, " hashs generated ",end='\r')
            old_h = [old_h[1], h]
            old_h_prime = [old_h_prime[1], h_prime]
        print(j, " hashs generated")
        #print("######### COLLISION #########\n H(" , old_h," ) = H( ", self.H(old_h_prime)," )\n#############################")
        #print("Proof : " , self.H(old_h) , " = ", self.H(self.H(old_h_prime)), "\n\n")
        return (h,j)

    def search_i0(self,h0, h0_pprime):
        '''
           Find the first value of i_0, ie when h_i = h''_i. (h is a sequence defined by : for all i, h_i = f(h_(i-1). See the paper for more info.)
        '''
        print("[*] STEP 1 finished with success. \n[*] STEP 2 ...")
        h = self.f(h0)
        h_pprime = self.f(h0_pprime)
        old_h = h0
        old_h_pprime = h0 # correspondent a h_{i-1}
        i = 1
        while h != h_pprime :
            old_h = h
            old_h_pprime = h_pprime
            h = self.f(h)
            h_pprime = self.f(h_pprime)
            if self.is_printing_hash:
                print("hash1=", h)
                print("hash2=", h_pprime)
            i+=1
            if i%100000 == 0:
                print(i, " hashs generated",end='\r')
        print(i, " hashs generated")
        return (i, old_h, old_h_pprime)

    def generateCollision(self):
        i0 = 0
        j0=0
        while i0 == 0 : # Tant que i0 = 0, on recommence avec un autre h0
            h0 = self.message_generator()
            print("\n\nRandom message generated =", h0)
            (h_pprime0,j0) = self.search_j0(h0)
            (i0, old_hi0,old_h_pprime_i0) = self.search_i0(h0, h_pprime0)# old_hi0 et old_h_pprime_i0 correspondent à h_{i0-1} et    h''_{i0-1}
        clear1 = self.R(old_hi0)
        clear2 = self.R(old_h_pprime_i0)
        print("\n\n\n################## COLLISION FOUND ##################\n\n" "Hash(",clear1, ") = ", str(self.hash_func(clear1)), "\nHash(",clear2, ") = ",str(self.hash_func(clear2)) ,"\n\n####################################################")
        return (clear1,clear2,i0+j0)
    
