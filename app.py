from flask import Flask, flash, render_template, request
import math
import string
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def main():
    method = request.form['01']  #check method

#choose the method
    if method == "method":
        return render_template('index.html', flash="alert: - select method")

    if request.form['form']=="encrypt":
    #caeser cipher
        if method == "caeser": 
            msg = request.form['input-plaintext']
            key = request.form['key']
            key = int(key)
            result = ""
            for char in msg:
                if char == " ": 
                    result += " "
                    continue
                if ord(char) > 96 :
                    result += chr((ord(char) + key - 97) % 26 + 97)

                else:
                    result += chr((ord(char)+ key - 65) % 26 +65)

            return render_template('index.html', output=result)
    
    #rail fence cipher
        elif method == "rail fence":
            s=request.form['input-plaintext']
            n=request.form['key']
            n=int(n)
            print(s)
            print(n)
            fence = [[] for i in range(n)]
            rail  = 0
            var = 1
            
            for char in s:
                fence[rail].append(char)
                rail += var
            
                if rail == n-1 or rail == 0:
                    var = -var
            
            res = ''
            for i in fence:
                for j in i:
                    res += j
            
            return render_template('index.html', output=res)
    
    #columner cipher
        elif method == "columner":
            s=request.form['input-plaintext']
            key=request.form['key']

            temp=[]
            for i in key:
                if i not in temp:
                    temp.append(i)
            k=""
            for i in temp:
                k+=i
            print("The key used for encryption is: ",k)
            

            b=math.ceil(len(s)/len(k))
            

            if(b<len(k)):
                b=b+(len(k)-b)

            arr=[['_' for i in range(len(k))]
                for j in range(b)]
            i=0
            j=0

            for h in range(len(s)):
                arr[i][j]=s[h]
                j+=1
                if(j>len(k)-1):
                    j=0
                    i+=1
            print("The message key is: ",key)
            # for i in arr:
            #     print(i)

            cipher_text=""

            kk=sorted(k)
            
            for i in kk:

                h=k.index(i)
                for j in range(len(arr)):
                    cipher_text+=arr[j][h]
            return render_template('index.html', output=cipher_text)

    #vigenere cipher
        elif method == "vigenere":
            plain_text=request.form['input-plaintext']
            key=request.form['key']
            main=string.ascii_lowercase
            index=0
            cipher_text=""
            plain_text=plain_text.lower()
            key=key.lower()
            for c in plain_text:
                if c in main:
                    off=ord(key[index])-ord('a')
                    encrypt_num=(ord(c)-ord('a')+off)%26
                    encrypt=chr(encrypt_num+ord('a'))
                    cipher_text+=encrypt
                    index=(index+1)%len(key)
                else:
                    cipher_text+=c

            print("plain text: ",plain_text)
            return render_template('index.html', output=cipher_text)

    #playfair cipher
        elif method == "playfair":
            key=request.form['key']

            main=string.ascii_lowercase.replace('j','.')

            key=key.lower()
            
            key_matrix=['' for i in range(5)]

            i=0;j=0
            for c in key:
                if c in main:

                    key_matrix[i]+=c


                    main=main.replace(c,'.')

                    j+=1

                    if(j>4):

                        i+=1

                        j=0

            for c in main:
                if c!='.':
                    key_matrix[i]+=c

                    j+=1
                    if j>4:
                        i+=1
                        j=0
                        
            print("Key Matrix for encryption:")
            print(key_matrix)




            plain_text=request.form['input-plaintext']

            plain_text_pairs=[]

            cipher_text_pairs=[]


            plain_text=plain_text.replace(" ","")

            plain_text=plain_text.lower()



            i=0

            while i<len(plain_text):

                a=plain_text[i]
                b=''

                if((i+1)==len(plain_text)):

                    b='x'
                else:

                    b=plain_text[i+1]

                if(a!=b):
                    plain_text_pairs.append(a+b)

                    i+=2
                else:
                    plain_text_pairs.append(a+'x')

                    i+=1
                    
            print("plain text pairs: ",plain_text_pairs)


            for pair in plain_text_pairs:

                flag=False
                for row in key_matrix:
                    if(pair[0] in row and pair[1] in row):

                        j0=row.find(pair[0])
                        j1=row.find(pair[1])
                        cipher_text_pair=row[(j0+1)%5]+row[(j1+1)%5]
                        cipher_text_pairs.append(cipher_text_pair)
                        flag=True
                if flag:
                    continue


                        
                for j in range(5):
                    col="".join([key_matrix[i][j] for i in range(5)])
                    if(pair[0] in col and pair[1] in col):

                        i0=col.find(pair[0])
                        i1=col.find(pair[1])
                        cipher_text_pair=col[(i0+1)%5]+col[(i1+1)%5]
                        cipher_text_pairs.append(cipher_text_pair)
                        flag=True
                if flag:
                    continue


                i0=0
                i1=0
                j0=0
                j1=0

                for i in range(5):
                    row=key_matrix[i]
                    if(pair[0] in row):
                        i0=i
                        j0=row.find(pair[0])
                    if(pair[1] in row):
                        i1=i
                        j1=row.find(pair[1])
                cipher_text_pair=key_matrix[i0][j1]+key_matrix[i1][j0]
                cipher_text_pairs.append(cipher_text_pair)
                
            print("cipher text pairs: ",cipher_text_pairs)

            print('plain text: ',plain_text)
            print('cipher text: ',"".join(cipher_text_pairs))
            # cipher_text="".join(cipher_text_pairs)

            return render_template('index.html', output="".join(cipher_text_pairs))

    #hill cipher
        elif method == "hill":
            main=string.ascii_lowercase

            def generate_key(n,s):
                s=s.replace(" ","")
                s=s.lower()
            
                key_matrix=['' for i in range(n)]
                i=0;j=0
                for c in s:
                    if c in main:
                        key_matrix[i]+=c
                        j+=1
                        if(j>n-1):
                            i+=1
                            j=0
                print("The key matrix "+"("+str(n)+'x'+str(n)+") is:")
                print(key_matrix)
            
                key_num_matrix=[]
                for i in key_matrix:
                    sub_array=[]
                    for j in range(n):
                        sub_array.append(ord(i[j])-ord('a'))
                    key_num_matrix.append(sub_array)
                
                for i in key_num_matrix:
                    print(i)
                return(key_num_matrix)
            

            def message_matrix(s,n):
                s=s.replace(" ","")
                s=s.lower()
                final_matrix=[]
                if(len(s)%n!=0):

                    while(len(s)%n!=0):
                        s=s+'z'
                print("Converted plain_text for encryption: ",s)
                for k in range(len(s)//n):
                    message_matrix=[]
                    for i in range(n):
                        sub=[]
                        for j in range(1):
                            sub.append(ord(s[i+(n*k)])-ord('a'))
                        message_matrix.append(sub)
                    final_matrix.append(message_matrix)
                print("The column matrices of plain text in numbers are:  ")
                for i in final_matrix:
                    print(i)
                return(final_matrix)



            def getCofactor(mat, temp, p, q, n):
                i = 0
                j = 0
            

                for row in range(n):  
                    for col in range(n):
                        

                        if (row != p and col != q) :
                            temp[i][j] = mat[row][col]
                            j += 1
            
            
                            if (j == n - 1):
                                j = 0
                                i += 1
            
            
            def determinantOfMatrix(mat, n):
                D = 0
            

                if (n == 1):
                    return mat[0][0]
                    

                temp = [[0 for x in range(n)]  
                        for y in range(n)]  
            
                sign = 1
            

                for f in range(n):
                    
            
                    getCofactor(mat, temp, 0, f, n)
                    D += (sign * mat[0][f] *
                        determinantOfMatrix(temp, n - 1))
            
            
                    sign = -sign
                return D
            
            def isInvertible(mat, n):
                if (determinantOfMatrix(mat, n) != 0):
                    return True
                else:
                    return False


            def multiply_and_convert(key,message):
            
            
                res_num = [[0 for x in range(len(message[0]))] for y in range(len(key))]
            
                for i in range(len(key)):
                    for j in range(len(message[0])):
                        for k in range(len(message)):

                            res_num[i][j]+=key[i][k] * message[k][j]

                res_alpha = [['' for x in range(len(message[0]))] for y in range(len(key))]

                for i in range(len(key)):
                    for j in range(len(message[0])):

                        res_alpha[i][j]+=chr((res_num[i][j]%26)+97)
                    
                return(res_alpha)


            n=int(3)
            s=request.form['key']
            key=generate_key(n,s)


            if (isInvertible(key, len(key))):
                print("Yes it is invertable and can be decrypted")
            else:
                print("No it is not invertable and cannot be decrypted")
            
            plain_text=request.form['input-plaintext']
            message=message_matrix(plain_text,n)
            final_message=''
            for i in message:
                sub=multiply_and_convert(key,i)
                for j in sub:
                    for k in j:
                        final_message+=k
            print("plain message: ",plain_text)
            print("final encrypted message: ",final_message)
            return render_template('index.html', output="".join(final_message))
    
    else:
        #caeser cipher
        if method == "caeser":
            text=str(request.form['input-plaintext'])
            s=int(request.form['key'])
            print(text)
            print(s)
            s=26-s 
                
            result=""  #empty string
            for i in range(len(text)):
                char=text[i]
                if(char.isupper()):  #if the text[i] is in upper case
                    result=result+chr((ord(char)+s-65)%26+65)
                else:
                    result=result+chr((ord(char)+s-97)%26+97)
            return render_template('index.html', output=result)
        
        #rail fence cipher
        elif method == "rail fence":
            def sequence(n):
                arr=[]
                i=0
            
                while(i<n-1):
                    arr.append(i)
                    i+=1
                while(i>0):
                    arr.append(i)
                    i-=1
                return(arr)

            cipher_text=request.form['input-plaintext']
            n=int(request.form['key'])

            cipher_text=cipher_text.lower()

            L=sequence(n)
            print("The raw sequence of indices: ",L)

            temp=L
            
            while(len(cipher_text)>len(L)):
                L=L+temp

            for i in range(len(L)-len(cipher_text)):
                L.pop()

            temp1=sorted(L)
            
            print("The row indices of the characters in the cipher string: ",L)

            print("The row indices of the characters in the plain string: ",temp1)
            
            print("Transformed message for decryption: ",cipher_text)

            plain_text=""
            for i in L:
                k=temp1.index(i)
                temp1[k]=n
                plain_text+=cipher_text[k]
            print("The cipher text is: ",plain_text)
            
            return render_template('index.html', output=plain_text)
               
        #columner cipher
        elif method == "columner":
            s=request.form['input-plaintext']
            key=request.form['key']
            print(s)
            print(key)
            temp=[]
            for i in key:
                if i not in temp:
                    temp.append(i)
            k=""
            for i in temp:
                k+=i
            print("The key used for encryption is: ",k)
            
            arr=[['' for i in range(len(k))]
                for j in range(int(len(s)/len(k)))]

            kk=sorted(k)
            
            d=0

            for i in kk:
                h=k.index(i)
                for j in range(len(k)):
                    arr[j][h]=s[d]
                    d+=1
                        
            print("The message matrix is: ")
            for i in arr:
                print(i)

            plain_text=""
            for i in arr:
                for j in i:
                    plain_text+=j
            print("The plain text is: ",plain_text)
            return render_template('index.html', output=plain_text)

        # #vigenere cipher
        elif method == "vigenere":

            s=request.form['input-plaintext']
            key=request.form['key']
            print(s)
            print(key)
            key_length = len(key)
            key_as_int = [ord(i) for i in key]
            ciphertext_int = [ord(i) for i in s]
            plaintext = ''
            for i in range(len(ciphertext_int)):
                value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
                plaintext += chr(value + 65)
            # return plaintext
            print("The plain text is: ",plaintext)
            return render_template('index.html', output=plaintext)

        # #playfair cipher
        elif method == "playfair":
            message=request.form['input-plaintext']
            key=request.form['key']
            print(message)
            print(key)
            
            def create_matrix(key):
                key = key.upper()
                matrix = [[0 for i in range (5)] for j in range(5)]
                letters_added = []
                row = 0
                col = 0
                # add the key to the matrix
                for letter in key:
                    if letter not in letters_added:
                        matrix[row][col] = letter
                        letters_added.append(letter)
                    else:
                        continue
                    if (col==4):
                        col = 0
                        row += 1
                    else:
                        col += 1
                #Add the rest of the alphabet to the matrix
                # A=65 ... Z=90
                for letter in range(65,91):
                    if letter==74: # I/J are in the same position
                            continue
                    if chr(letter) not in letters_added: # Do not add repeated letters
                        letters_added.append(chr(letter))
                        
                #print (len(letters_added), letters_added)
                index = 0
                for i in range(5):
                    for j in range(5):
                        matrix[i][j] = letters_added[index]
                        index+=1
                return matrix

            def separate_same_letters(message):
                index = 0
                while (index<len(message)):
                    l1 = message[index]
                    if index == len(message)-1:
                        message = message + 'X'
                        index += 2
                        continue
                    l2 = message[index+1]
                    if l1==l2:
                        message = message[:index+1] + "X" + message[index+1:]
                    index +=2   
                return message

            #Return the index of a letter in the matrix
            #This will be used to know what rule (1-4) to apply
            def indexOf(letter,matrix):
                for i in range (5):
                    try:
                        index = matrix[i].index(letter)
                        return (i,index)
                    except:
                        continue

            #Implementation of the playfair cipher
            #If encrypt=True the method will encrypt the message
            # otherwise the method will decrypt
            def playfair(key, message, encrypt=True):
                inc = 1
                if encrypt==False:
                    inc = -1
                matrix = create_matrix(key)
                message = message.upper()
                message = message.replace(' ','')    
                message = separate_same_letters(message)
                cipher_text=''
                for (l1, l2) in zip(message[0::2], message[1::2]):
                    row1,col1 = indexOf(l1,matrix)
                    row2,col2 = indexOf(l2,matrix)
                    if row1==row2: #Rule 2, the letters are in the same row
                        cipher_text += matrix[row1][(col1+inc)%5] + matrix[row2][(col2+inc)%5]
                    elif col1==col2:# Rule 3, the letters are in the same column
                        cipher_text += matrix[(row1+inc)%5][col1] + matrix[(row2+inc)%5][col2]
                    else: #Rule 4, the letters are in a different row and column
                        cipher_text += matrix[row1][col2] + matrix[row2][col1]

            playfair(key,message,False)

            print("The plain text is: ",message)
            return render_template('index.html', output=message)

        # #hill cipher
        #elif method == "hill":
            
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000, debug=True)