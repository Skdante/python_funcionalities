import JsonFunctions as js

if __name__ == '__main__':
    try:
        objCFG = js.fnLoadCFGJSON('datas.json')
        if objCFG != None: 
            print(objCFG["SQL"]["connection"]["connectionstr"])
        else:
             print('---|||||| JSON Invalid ||||||---')
    except Exception as e:
        print('---|||||| ERROR: ' + str(e) + ' ||||||---')