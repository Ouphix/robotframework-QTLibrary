# -*- coding: cp936 -*-
#encoding=utf-8

import datetime
from datetime import date
import re
import os
import time
import socket
import urlparse
import random
import string
import codecs
import sys
try:
    import subprocess
except ImportError:
    subprocess = None  # subprocess not available on Python/Jython < 2.5

__version__ = '0.10'


class _ElementKeywords():

    def __init__(self):
        self._counter = 0
        """self._element_finder = ElementFinder()"""
        pass
    # Public, element lookups

    def count(self):
        """Simulates moving mouse away from the element specified by `locator`.
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        | test | test2 |
        Example:
        | Execute JavaScript | window.my_js_function('arg1', 'arg2') |
        | Execute JavaScript | ${CURDIR}/js_to_execute.js |
        """
        self._counter += 1
        return self._counter

    def clear_counter(self):
        """clear counter has only a short documentation"""
        self._counter = 0
    def gen_nums(self,counts):
        """Get random number string.
        Example:
        | @{a}= | gen nums | 4 |
        It will return 4 random number. like '2624','1456'.
        """

        li = string.digits
        s = ''
        for n in range(0,int(counts)) :
            s += li[random.randint(0,len(li)-1)]
        return s
    def gen_chars(self,counts,upper='M'):
        """Get random character string.
        upper=U, will get all upper chars.
        upper=L, will get all lower chars.
        upper=M, will get mixed upper and lower chars.
        Example:
        | @{a}= | gen chars | 4 | U |
        It will return 4 random number. like 'ABCS','FDWW'.
        """
        s = ''
        #print string.ascii_letters
        if upper.upper() == 'U':
            li = string.ascii_uppercase
            lenli = len(li)
            for n in range(0,int(counts)):
                s += li[random.randint(0,lenli-1)]
        elif upper.upper() == 'L':
            li = string.ascii_lowercase
            lenli = len(li)
            for n in range(0,int(counts)):
                s += li[random.randint(0,lenli-1)]
        elif upper.upper() == 'M':
            li = string.ascii_letters
            lenli = len(li)
            for n in range(0,int(counts)):
                s += li[random.randint(0,lenli-1)]
        else :
            pass
        return s
    def gen_birthday(self,maxAge=55,minAge=21,sep=''):
        """Get random birthday.
        Example:
        | @{a}= | gen birthday | 4 | 0 | - |
        It will return random age in 0-4 years old birthday.
        like '20100302','20120123'.
        If sep is not null, such as '-', it will return '2010-03-02'
        """
        now = date.today()
        #print now
        birth = now.year - int(minAge)
        #print birth
        mon      = ['1','2','3','4','5','6','7','8','9','10','11','12']
        mon_days = ['31','28','31','30','31','30','31','31','30','31','30','31']
        s =''
        age = int(maxAge)-int(minAge)
        #print 'age'+str(age)
        y = str(birth - random.randint(1,age))
        #print 'y'+str(y)
        index1 = random.randint(0,11)
        #print 'index1:'+str(index1)
        m = str(mon[index1])
        m = m.zfill(2)
        maxDay = int(mon_days[index1])
        d = str(random.randint(1,maxDay))
        d = d.zfill(2)
        s = y + sep + m + sep + d
        return s
    def gen_idcard(self,idcard='',maxAge=55,minAge=21):
        """Get idcard No.
        Example:
        | @{a}= | gen idcard | 123 |
        It will return random idcard.
        like '111110198101010231','111110198402010231'.
        If the lenth of idcard in (15,17,18),
            it will return 18-idcard No
        Else
            it will return random 18-idcard No (21<age<55)
        """
        idlen=len(idcard)
        ic=str(idcard)
        if idlen==17 :
            pass
        elif idlen==15 :
            ic=ic[0:6]+'19'+ic[6:15]
        elif idlen==18 :
            pass
        else :
            ic=self.gen_nums(6)+self.gen_birthday(int(maxAge),int(minAge),'')+self.gen_nums(3)
            #print ic
        ic = ic[0:17]
        lid = list(ic)
        temp = 0
        for nn in range(2,19):
            #print 'nn:'+str(nn)
            a=int(lid[18-nn])
            w= (2**(nn-1)) % 11
            #print 'w:'+str(w)
            temp+=a*w
            #print temp
        temp = (12-temp % 11) % 11 
        if temp >=0 and temp <=9 :
            ic+=str(temp)
        elif temp ==10 :
            ic+='X'
        return ic

    #������֤����
    def verify_idcard(self,idcard):
        """verify 18-idcard.
        Example:
        | @{a}= | verify birthday | 111110198101010231 |
        It will return true or false for the idcard.
        """
        #print idcard
        #Ȩ������
        iW = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1];
        #���֤�����п��ܵ��ַ�
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x']
        #ʹ��������ʽ���
        icre = re.compile('^[1-9][0-9]{16}[x0-9]$', re.IGNORECASE);
        m = icre.match(idcard);
        if m:
            pass; 
        else:
            #���ǺϷ������֤���룬ֱ���˳�
            return unicode('���ǺϷ������֤����','gbk');
 
        S = 0;
        for i in range(0,17):
            S += int(idcard[i]) * iW[i];
 
        chk_val = (12 - (S % 11)) % 11;
        return idcard[17].lower() == values[chk_val];

    def _lapd_str(self,strings,lens,char):
        tlen=len(strings)
        s = ''
        if tlen<lens :
            for n in range(1,lens-tlen):
                s+=char
            s+=strings
        else :
            s=strings
        return s

    def _Unicode(self):
        val = random.randint(0x4E00, 0x9FBF)
        return unichr(val)

    def gen_name(self,num=3):
        """gen_name gen chinese name.
        Example:
        | @{a}= | gen name | 3 |
        It will return chinese name.
        """        
        #�����б�
        li_name =[u'��',u'Ǯ',u'��',u'��',u'��',u'��',u'֣',u'��',u'��',u'��',u'��',u'��',
									u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'ʩ',u'��',u'��',u'��',u'��',
									u'��',u'��',u'��',u'��',u'κ',u'��',u'��',u'��',u'л',u'��',u'��',u'��',
									u'ˮ',u'�',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'³',
									u'Τ',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'Ԭ',u'��',u'ۺ',
									u'��',u'ʷ',u'��',u'��',u'��',u'�',u'Ѧ',u'��',u'��',u'��',u'��',u'��',
									u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'ʱ',u'��',u'Ƥ',
									u'��',u'��',u'��',u'��',u'��',u'Ԫ',u'��',u'��',u'��',u'ƽ',u'��',u'��',
									u'��',u'��',u'��',u'Ҧ',u'��',u'��',u'��',u'��',u'ë',u'��',u'��',u'��',
									u'��',u'��',u'�',u'��',u'��',u'��',u'��',u'̸',u'��',u'é',u'��',u'��',
									u'��',u'��',u'��',u'��',u'ף',u'��',u'��',u'��',u'��',u'��',u'��',u'ϯ',
									u'��',u'��',u'ǿ',u'��',u'·',u'¦',u'Σ',u'��',u'ͯ',u'��',u'��',u'÷',
									u'ʢ',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',
									u'��',u'��',u'��',u'��',u'��',u'֧',u'��',u'��',u'��',u'¬',u'Ī',u'��',
									u'��',u'��',u'��',u'��',u'��',u'Ӧ',u'��',u'��',u'��',u'��',u'��',u'��',
									u'��',u'��',u'��',u'��',u'��',u'��',u'ʯ',u'��',u'��',u'ť',u'��',u'��',
									u'��',u'��',u'��',u'��',u'��',u'½',u'��',u'��',u'��',u'��',u'�',u'��',
									u'κ',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',
									u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'ɽ',u'��',u'��',
									u'��',u'�',u'��',u'ȫ',u'ۭ',u'��',u'��',u'��',u'��',u'��',u'��',u'��',
									u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',
									u'ղ',u'��',u'��',u'��',u'Ҷ',u'��',u'˾',u'��',u'۬',u'��',u'��',u'��',
									u'ӡ',u'��',u'��',u'��',u'��',u'̨',u'��',u'��',u'��',u'��',u'��',u'��',
									u'׿',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'˫',
									u'��',u'ݷ',u'��',u'��',u'̷',u'��',u'��',u'��',u'��',u'��',u'��',u'��',
									u'Ƚ',u'��',u'۪',u'Ӻ',u'ȴ',u'�',u'ɣ',u'��',u'�',u'ţ',u'��',u'ͨ',
									u'��',u'��',u'��',u'��',u'ۣ',u'��',u'��',u'ũ',u'��',u'��',u'ׯ',u'��',
									u'��',u'��',u'��',u'��',u'Ľ',u'��',u'��',u'ϰ',u'��',u'��',u'��',u'��',
									u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',
									u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'»',u'��',u'��',
									u'Ź',u'�',u'��',u'��',u'ε',u'Խ',u'��',u'¡',u'��',u'��',u'��',u'��',
									u'ʦ',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',
									u'��',u'��',u'ɳ',u'ؿ',u'��',u'��',u'��',u'��',u'��',u'��',u'��',u'��',
									u'��',u'��',u'��',u'��',u'��',u'��',u'Ȩ',u'��',u'��',u'��',u'��',u'��',
									u'��',u'ٹ',u'˾��',u'�Ϲ�',u'ŷ��',u'�ĺ�',u'���',u'����',u'����',u'����',u'�ʸ�',u'ξ��',
									u'����',u'�̨',u'��',u'ұ',u'��',u'��',u'�',u'��',u'����',u'����',u'̫��',u'��',
									u'��',u'����',u'����',u'��ԯ',u'���',u'����',u'����',u'����',u'Ľ��',u'����',u'����',u'˾ͽ',
									u'˾��',u'����',u'˾��',u'�붽',u'�ӳ�',u'���',u'��ľ',u'��',u'��',u'����',u'���',u'����',
									u'����',u'����',u'�ؼ�',u'����',u'����',u'��',u'��',u'��',u'��',u'��',u'��',
									u'۳',u'Ϳ',u'��',u'��',u'��',u'����',u'����',u'����',u'����',u'�麣',u'����',u'΢��',
									u'��',u'˧',u'�ÿ�',u'��',u'��',u'����',u'��',u'��',u'����',u'����',u'����',u'��',
									u'Ĳ',u'��',u'٦��',u'��',u'�Ϲ�',u'ī��',u'����',u'��',u'��',u'��',u'١']
        ln = len(li_name)
        last_name= li_name[random.randint(0,ln-1)]
        #print last_name
        first_name =''
        for n in range(0,int(num)-len(last_name)):
            first_name += self._GB2312()
            #print first_name
        return last_name + first_name

    #@������ɺ���
    def _GB2312(self):
        
        str1 = self._hex()
        #print 'str1:'+str1
        #print str1.decode('hex')
        try :
            str2 =str1.decode('hex').decode('gb2312')
        except UnicodeDecodeError:
            #���ִ����ʱ����������һ������
            str1 = self._hex()
            try :
                str2 =str1.decode('hex').decode('gb2312')
                #print '22222' + str2
            except UnicodeDecodeError:
                #��һRP�ܲ�Ǳ����Ǿ�ָ��һ����������
                str2 = u'��'
        return str2
    
    def _hex(self):
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        if body == 0xF :
            tail = random.randint(0, 0xE)
        else :
            tail = random.randint(0, 0xF)
        val = ( head << 8 ) | (body << 4) | tail
        str1 = "%x" % val
        return str1
    
    def create_pboc(self, new_name,new_id,filepath):
        """Create Pboc
        You can create a normal credit file by using this keyword.
        Example:
        Create Pboc| Pingan | 252461196308226269|${CURDIR}
        It will create a credit file in the directory and return the file path
        Then you can upload the file.
        Remember that ${CURDIR} is necessary!! :b
        """

        path_sep=os.sep
        credit_file=filepath+path_sep+'credit.html'
        #print credit_file
        lines = open(credit_file, "rb").readlines()
        tmp=lines[0].strip()
        cust_name = re.compile('id="custName" type="hidden" value="(.*?)"/>').findall(tmp)[0]
        #print cust_name
        tmp=lines[1].strip()
        cust_id = re.compile('id="custId" type="hidden" value="(.*?)"/>').findall(tmp)[0]
        #print cust_id
        tmp=lines[2].strip()
        credit_id = re.compile('id="credit_id" type="hidden" value="(.*?)"/>').findall(tmp)[0]
        #print credit_id
        new_creditid=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        new_creditid+=str(datetime.datetime.now().microsecond)
        new_creditid+=str(random.randint(10,99))
        #Get Customer Name And ID in the Credit File
        new_id=new_id.encode("GBK")
        new_name=new_name.encode("GBK")
        #Convert it into GBK code
        streamWriter = codecs.lookup('utf-8')[-1]
        sys.stdout=open(credit_file,"r")
        sys.stdout = streamWriter(sys.stdout)
        content=sys.stdout.read().replace(cust_name,new_name).replace(cust_id,new_id).replace(credit_id,new_creditid)
        f = open(credit_file,'w')
        f.write(content)
        #Replace the Name and ID 
        f.close()
        sys.stdout.close()
        return credit_file

if __name__ == "__main__":
    #����һ�������õĽű�������ֱ�����и��ļ���֤�����ĺ���
    #�ⲿ�ֵĴ����Ͻ�ɾ��
    #u=_ElementKeywords().Unicode()
    #print u
    #x=_ElementKeywords()._GB2312()
    #print x
    for n in range(0,100):
        na=_ElementKeywords().gen_name(4)
        print na
    """a=_ElementKeywords().gen_birthday('23','21','-')
    print 'a:'+a
    b=_ElementKeywords().gen_idcard('')
    print 'b:'+b
    c=_ElementKeywords().verify_idcard(b)
    print 'c:'+str(c)
    d=_ElementKeywords().gen_nums(5)
    print 'd:'+d
    e=_ElementKeywords().gen_chars(6)
    print 'e:'+e"""



