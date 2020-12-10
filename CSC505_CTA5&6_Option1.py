import pandas as pd
pd.set_option('display.max_columns',None)

#Import Module with Menu class variables and methods
from HoleMod import UserLog as U
from HoleMod import PHReporter as R
from HoleMod import Employee as E

#Import the prior save of the inventory file and user file
from ImportCrew import crews
Crew=crews
from ImportUser import users
Users=users
from ImportReport import pothole_reports
Report=pothole_reports
from DamageList import damages
DamageReport=damages
from WorkOrders import work_orders
WOList=work_orders

#This function is designed to export data to a .py file so that existing inventory can be reloaded at the start of each program re-boot
def Export_File(inventory,file,title):
    with open(file,'w') as data2:
        data2.write('%s = { \n' %title)
        for k in inventory.keys():
            data2.write(" '%s' : %s, \n" % (k, inventory[k]))
        data2.write("}")

#Extract User LogIn from details
def getkey(dict):
    list = []
    for key in dict.keys():
        list.append(key)
    return list

login_list=getkey(Users)
hole_log=getkey(Report)
selection=True

#For the purposes of testing, I am making user logins available
#This would be removed in a production version
print(login_list)
#Reporting Program Main
print('Welcome to the Pothole Tracking and Repair System (PHTRS)')
print('User Names are formatted using the first initial of your firstname, full last name,')
print('and the last 4 digits of your phone number (ex bsmith1234).')
selection=str(input('Please Enter your Log In:'))
if selection not in login_list:
    s,u=U().NewUser(selection)
    selection=s
    Users[s]=u
    Export_File(Users,'ImportUser.py','users')

print('Welcome '+Users[selection][0],''+Users[selection][1])
#Menu for program main
if Users[selection][7]=='n':
    print('We appreciate our citizens reporting area potholes to us.')
    hole=input('Please provide the street address for the pothole you wish to report:')
    hole=hole.title()
    if hole not in hole_log:
        rep,dam=R().ReportNew(hole,Users[selection],Report)
    else:
        rep,dam=R().ReportExisting(Report,hole,Users[selection])
    Report=rep
    DamageReport=dam
    Export_File(Report,'ImportReport.py','pothole_reports')
    Export_File(DamageReport,'DamageList.py','damages')
    wol=E().Work_Order_Assign(WOList,Report)
    WOList=wol
    Export_File(WOList,'WorkOrders.py','work_orders')
else:
    option=1
    while option:
        print('Welcome to the Employee Reporting System. Please Make a Selection:')
        print('1) Report a Pothole.')
        print('2) View Work Orders by Priority.')
        print('3) Update Work Orders.')
        print('4) View Damage Reports.')
        print('5) Update Damage Reports.')
        print('6) Exit the program.')
        option=input('Please select an option:')
        #Selection 1-Option for Employee to report potholes/damages
        if option =='1':
            hole=input('Please provide the street address for the pothole you wish to report:')
            hole=hole.title()
            if hole not in hole_log:
                rep,dam=R().ReportNew(hole,Users[selection],Report)
            else:
                rep,dam=R().ReportExisting(Report,hole,Users[selection])
            Report=rep
            DamageReport=dam
            Export_File(Report,'ImportReport.py','pothole_reports')
            Export_File(DamageReport,'DamageList.py','damages')
            wol=E().Work_Order_Assign(WOList,Report)
            WOList=wol
            Export_File(WOList,'WorkOrders.py','work_orders')
        #Selection 2-Screen Printout of Work Orders.
        elif option =='2':
            prio_wo=E().Prioritize(WOList,Crew,Report)
            df_wo=pd.DataFrame(prio_wo).transpose()
            df_wo.columns=['WO#','Incident Addr','Crew Assigned','Hrs Worked','Vol Filler','Cost Incurred','Rep Status','Hole Size','Tools Assigned']
            print(df_wo)
        #Selection 3-Update a Work Order.
        elif option =='3':
            uwo=input('Please provide the Work Order number you wish to update:')
            E().Work_Order_Update(uwo,WOList)
            Export_File(WOList,'WorkOrders.py','work_orders')
        #Selection 4-View the Damage Reports.
        elif option =='4':
            df=pd.DataFrame(DamageReport).transpose()
            df.columns=['Incident Addr','Owner','Own Address','Own Phone','Damage Type','Own(1)/Pass(2)','Damage Location','Cost to Rep','Rep Status']
            print(df)
        #Selection 5-Update the Damage Reports as Paid.
        elif option =='5':
            dr=input('Provide the incident number for the damage you wish to pay:')
            dmg=E().Damage_Update(dr,DamageReport)
            Export_File(dmg,'DamageList.py','damages')
        #Selection 6-Exit
        elif option =='6':
            print('Exiting')
            break
        #Error control
        else:
            print('Please give a valid option.')
            continue



