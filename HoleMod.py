#Blocks of repetitive code that are useful functions, but not directly attributed to the classes, so are outside of them.
def Export_File(inventory,file,title):
    with open(file,'w') as data2:
        data2.write('%s = { \n' %title)
        for k in inventory.keys():
            data2.write(" '%s' : %s, \n" % (k, inventory[k]))
        data2.write("}")

def getkey(dict):
    list = []
    for key in dict.keys():
        list.append(key)
    return list

#Initialize my User Log class
class UserLog:
    def __init__(self):
        self.fn=''
        self.ln=''
        self.ad=''
        self.cy=''
        self.st='TX'
        self.un=''
        self.em='n'
        self.login=''

    #Function to add a new user
    def NewUser(self,login):
        self.login=login
        x='n'
        this_user=''
        new_list=[]
        while x=='n':
            fn=str(input('You appear to be a new user. We will create your account starting with your First Name:'))
            fn=fn.title()
            ln=str(input('Last Name:'))
            ln=ln.title()
            ad=str(input('Street Address:'))
            ad=ad.title()
            cy=str(input('City:'))
            cy=cy.title()
            st='TX'
            zp=str(input('Zip Code:'))
            ph=str(input('Phone Number (xxx-xxx-xxxx):'))
            un=fn[0].lower()+ln.lower()+ph[8:12]
            em=str(input('Do you work for the city? Y/N'))
            em=em.lower()
            this_user=un
            new_list=[fn,ln,ad,cy,st,zp,ph,em]
            print('User Names are formatted using the first initial of your firstname, full last name,')
            print('and the last 4 digits of your phone number (ex bsmith1234).')
            print('Your user name is: %s' %un)
            x=(input('Please type Y to confirm or N to reenter info:'))
            x=x.lower()
        return (this_user, new_list)

#Initialize my Reporter class
class PHReporter:
    def __init__(self):
        self.hole=''
        self.damage=''
        self.d=0
        self.l=''
        self.p=0
        self.c=0
        self.damage_dict={}
        self.user={}
        self.selection=''

    def AddOwnerData(self,user):
        self.user=user

        who=user[0]+' '+user[1]
        where=user[2]+' '+user[3]+' '+user[4]+' '+user[5]
        phone=user[6]
        return who,where,phone

    def ReportDamage(self,hole,user):
        self.hole=hole
        damage_dict={}
        z=0
        type=''
        l=''
        p=''
        cost=0
        damage=input('Did you incur damages or injuries from this pothole?')
        damage=damage.lower()
        while damage=='y':
            print('What kind of Damage? Select from:')
            print('1- Vehicle')
            d=int(input('2- Bodily Injury'))
            if d==1:
                type='Vehicle'
                l=input('Briefly describe where on the vehicle the damage is:')
                p=1
                cost=float(input('What was the cost to repair this damage?'))
            elif d==2:
                type='Body'
                p=int(input('Who was injured? \n1=Vehicle owner \n2=passenger'))
                if p not in [1,2]:
                    p=input('Please enter a valid selection:')
                l=input('Briefly describe where on the body the injury occured:')
                cost=float(input('What was the total cost of medical bills, unpaid work, etc incurred from this injury?'))
            else:
                print('That is not a valid selection.')
                continue
            wh,pl,ph=PHReporter().AddOwnerData(user)
            z=z+1
            damage_dict[z]= [hole,wh,pl,ph,type,p,l,cost,'unpaid']
            x=input('Was there other damage? Y/N')
            damage=x.lower()
        else:
            print('Thank you for your report.  Goodbye.')
        return damage_dict

    def ReportExisting(self,inventory,hole,user):
        self.inventory=inventory
        self.hole=hole
        self.user=user

        rkey=getkey(inventory)

        for x in inventory.values():
            if hole in rkey:
                print('We have this pothole on record, but will add your complaint.')
                x[3]=x[3]+1
            damage_report=PHReporter().ReportDamage(hole,user)
            break
        return inventory,damage_report

    def ReportNew(self,hole,user,inventory):
        self.hole=hole
        self.user=user
        self.inventory=inventory
        print('This hole has not be previously reported.')
        size=int(input('On a scale of 1-10, describe the size of the hole:'))
        loc=input('Briefly describe where in the street the hole is located (side,center,etc):')
        dis=5
        comp=1
        print('Thank you for reporting to us.  This has been logged.')
        inventory[hole]=[size,loc,dis,comp]
        damage_report=PHReporter().ReportDamage(hole,user)
        return inventory,damage_report

class Employee:
    def __init__(self):
        self.incident=0
        self.report={}
        self.inventory={}
        self.wolist=[]

    def Damage_Update(self,incident,report):
        self.incident=incident
        self.report=report
        x='y'
        while x=='y':
            if incident in report.keys():
                report[incident][8]='paid'
                z=input('Are there other incidents you want to pay?')
                x=z.lower()
            else:
                print('Please enter a valid option')
                continue
        return report

    def Work_Order_Assign(self,wolist,inventory):
        self.wolist=wolist
        self.inventory=inventory
        wkey=getkey(inventory)
        z=len(wolist)
        lcs=[]
        for y in wolist:
            lcs.append(wolist[y][0])
        for x in wkey:
            if x not in lcs:
                loc=x
                z=z+1
                if inventory[x][0] >= 5:
                    crew=2734
                else:
                    crew=2755
                hrs=0
                mvol=0
                cost=0
                stat='Not Repaired'
                wolist[z]=[loc,crew,hrs,mvol,cost,stat]
        return wolist

    def Combo_WO(self,wol,crl,rpl):
        self.wol=wol
        self.crl=crl
        self.rpl=rpl
        bigwo=wol
        for x in bigwo:
            if bigwo[x][0] in rpl.keys():
                bigwo[x].append(int(rpl[bigwo[x][0]][0]))
            if bigwo[x][1] in crl.keys():
                bigwo[x].append("backhoe and "+crl[bigwo[x][1]][2])
        return bigwo

    def Prioritize(self,wod,crd,rpd):
        self.wod=wod
        self.crd=crd
        self.rpd=rpd
        stat_NR={}
        stat_WP={}
        stat_TR={}
        stat_FR={}

        def prio(d):
            list=[]
            prio_d={}
            for key in d:
                list.append(d[key][6])
            list=sorted(list,reverse=True)
            for x in range(len(list)):
                for k,v in d.items():
                    key=k
                    value=v
                    if list[x]==d[k][6]:
                        prio_d[x+1]=v
                        prio_d[x+1].insert(0,k)
            return prio_d
        def addon(add,final):
            for x in add:
                y=len(final)
                final[y+1]=add[x]
            return final

        bdict=Employee().Combo_WO(wod,crd,rpd)
        for x in bdict:
            if bdict[x][5]=='Not Repaired':
                stat_NR[x]=bdict[x]
            elif bdict[x][5]=='Work in Progress':
                stat_WP[x]=bdict[x]
            elif bdict[x][5]=='Temp Repair':
                stat_TR[x]=bdict[x]
            elif bdict[x][5]=='Repaired':
                stat_FR[x]=bdict[x]
            else:
                pass
        NR=prio(stat_NR)
        WP=prio(stat_WP)
        TR=prio(stat_TR)
        FR=prio(stat_FR)
        final_prio=NR.copy()
        final_prio=addon(WP,final_prio)
        final_prio=addon(TR,final_prio)
        final_prio=addon(FR,final_prio)
        return final_prio



    def WO_Status(self,wost):
        self.wost=wost

        print('To update the status please select new status from list:')
        print('1) Work in Progress')
        print('2) Temporary Repair Complete')
        print('3) All Repair Work is Complete')
        stat=int(input('4) No Changes to Status'))
        if stat==1:
            wost='Work in Progress'
        elif stat==2:
            wost='Temp Repair'
        elif stat==3:
            wost='Repaired'
        elif stat==4:
            pass
        else:
            print('Please select a valid option')
        return wost

    def WO_Work_Update(self,wo):
        self.wo=wo

        if wo[5] != 'Not Repaired':
            hrs=float(input('Please enter the hours of work for this job:'))
            mat=float(input('Please enter the volume of filler used for this job (in cu ft):'))
        return hrs,mat

    from ImportCrew import crews
    Crew=crews

    def WO_Cost_Calc(self,wo,crew):
        self.wo=wo
        self.crew=crew
        wcost=0
        eqcost=0
        mcost=float(wo[3]*1.5)
        if wo[1]==2734:
            wcost=float(crew[2734][0]*wo[2]*20)
            eqcost=float((wo[2]*15)+(wo[2]*12))
        elif wo[1]==2755:
            wcost=float(crew[2755][0]*wo[2]*20)
            eqcost=float((wo[2]*15)+(wo[2]*45))
        else:
            print('The Crew assigned is invalid, please update the WO')
        tcost=mcost+wcost+eqcost
        return tcost


    def Work_Order_Update(self,wonum,report):
        self.wonum=wonum
        self.report=report
        x='y'

        while x=='y':
            if wonum in report.keys():
                print('You have requested to update WO# %s' % wonum)
                print('The current status is:')
                print('   Location        Crew  Spend   Status')
                print(report[wonum])
                fix=Employee().WO_Status(report[wonum][5])
                report[wonum][5]=fix
                h,m=Employee().WO_Work_Update(report[wonum])
                report[wonum][2]=h
                report[wonum][3]=m
                c=Employee().WO_Cost_Calc(report[wonum],Employee.Crew)
                report[wonum][4]=c
                x='n'
            else:
                print('Please enter a valid option')
                x='n'
        return report

