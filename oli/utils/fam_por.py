

def write_odm_line( oc_item_name, ls_item_value, is_date=False, is_time=False, is_decimal=False, is_integer=False, is_utf8 = False):
    _one_line = ''
    if (ls_item_value):
        _this_value = ls_item_value
        if (is_date):
            _this_value = ls_item_value[0:10]
        if (is_time):
            # time field: for now we do nothing with it
            _this_value = _this_value           
        if (is_decimal):
            try:
                float(ls_item_value)
                _this_value = str(ls_item_value)
            except:
                _this_value = 'CONVERSION-ERROR %s value %s to float' % (oc_item_name, ls_item_value)
        if (is_integer):
            try:
                int(ls_item_value)
                _this_value = str(ls_item_value)
            except:
                _this_value = 'CONVERSION-ERROR %s value %s to integer' % (oc_item_name, ls_item_value)
        if (is_utf8):
            _this_value = str(_this_value.encode(encoding="ascii",errors="xmlcharrefreplace"))
            # now we have something like b'some text &amp; more' so we want to loose the first two characters and the last one
            # TODO: make this nicer somehow
            _this_value = _this_value[2:]
            _this_value = _this_value[:-1]
            # and finally, replace double quotes with &quot;
            _this_value = _this_value.replace('"', '&quot;')  
                 
        _one_line = _one_line + '            <ItemData ItemOID="' + oc_item_name + '" Value="' + _this_value + '"/>'
    else:
        _one_line = _one_line + '            <ItemData ItemOID="' + oc_item_name + '" Value=""/>'
    #print(_one_line)
    return _one_line

def compose_odm(study_subject_oid, data_odk):
    """
    compose the xml-content to send to the web-service 
    just for this one occasion we write out everything literally
    and we make a big exception for birth-weight, which is given 
    in grams, but must be imported in kilo's and grams 
    """
    #print('in compose_odm ', study_subject_oid)
    if (data_odk['q5birthweightgram'] is not None):
        kilograms = int(float(data_odk['q5birthweightgram'])/1000)
        if(kilograms == 0):
            I_PTFAM_BIRTHWEIGHTKG = ''
        else:
            I_PTFAM_BIRTHWEIGHTKG = str(kilograms)
        grams = int(float(data_odk['q5birthweightgram']) - kilograms * 1000)
        I_PTFAM_BIRTHWEIGHTGR = str(grams)
        #print(data_odk['q5birthweightgram'], I_PTFAM_BIRTHWEIGHTKG, I_PTFAM_BIRTHWEIGHTGR)
    else:
        I_PTFAM_BIRTHWEIGHTKG = ''
        I_PTFAM_BIRTHWEIGHTGR = ''
    
    # opening tags
    _odm_data = ''
    _odm_data = _odm_data + '<ODM>'
    _odm_data = _odm_data + '  <ClinicalData StudyOID="S_CPPOR">'
    _odm_data = _odm_data + '    <SubjectData SubjectKey="' + study_subject_oid + '">'
    _odm_data = _odm_data + '      <StudyEventData StudyEventOID="SE_POR_CP">'
    _odm_data = _odm_data + '        <FormData FormOID="F_PTFAMILYFORM_V12">'
    _odm_data = _odm_data + '          <ItemGroupData ItemGroupOID="IG_PTFAM_UNGROUPED" ItemGroupRepeatKey="1" TransactionType="Insert">'
    # data section 1
    _odm_data = _odm_data + write_odm_line('I_PTFAM_RELATIONSHIP', data_odk['q1relationship'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_RELATIONSHIPOTH', data_odk['q1relationshipother'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_DATEOFBIRTHCOMPLETE', data_odk['q3birthdatecomplete'], is_date=True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_GENDER', data_odk['q4sex'])
    # begin first exception !
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BIRTHWEIGHTKG', I_PTFAM_BIRTHWEIGHTKG)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BIRTHWEIGHTGR', I_PTFAM_BIRTHWEIGHTGR)
    # end first exception

    _odm_data = _odm_data + write_odm_line('I_PTFAM_LATEEARLYBIRTH', data_odk['q6fullterm'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BREASTFEDEVER', data_odk['q7breastfed'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BREASTFEDHOWLONG', data_odk['q7breastfedmonths'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BREASTEXCLEVER', data_odk['q8breastfedexclusive'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BREASTEXCLUSIVE', data_odk['q8breastexclusive'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FORMULAMILK', data_odk['q08cformulamilk'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FORMULAMILSTART', data_odk['q08dformulamilkstart'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_COMPLFEEDINGSTART', data_odk['q08dcomplementaryfee'], is_integer = True)

    # data section 2
    _odm_data = _odm_data + write_odm_line('I_PTFAM_DISTANCESCHOOLHOME', data_odk['q9distance'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_TRANSPSCHOOLTO', data_odk['q10transpschoolto'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_TRANSPSCHOOLFROM', data_odk['q10transpschoolfrom'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WALKINGCYCLINGTIMETO', data_odk['q10bwalkcycletimeto'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WALKINGCYCLINGTIMEFROM', data_odk['q10bwalkcycletimefro'], is_integer = True)

    q10areasonmotorized = ''
    if (data_odk['q10areasonmotorized[1]'] == 'Y'):
        q10areasonmotorized = q10areasonmotorized + '1,'
    if (data_odk['q10areasonmotorized[2]'] == 'Y'):
        q10areasonmotorized = q10areasonmotorized + '2,'
    if (data_odk['q10areasonmotorized[3]'] == 'Y'):
        q10areasonmotorized = q10areasonmotorized + '3,'
    if (data_odk['q10areasonmotorized[4]'] == 'Y'):
        q10areasonmotorized = q10areasonmotorized + '4,'
    if (data_odk['q10areasonmotorized[5]'] == 'Y'):
        q10areasonmotorized = q10areasonmotorized + '5,'
    if (q10areasonmotorized != '' and q10areasonmotorized[-1] ==','):
        q10areasonmotorized = q10areasonmotorized[0: (len(q10areasonmotorized) -1)]
    _odm_data = _odm_data + write_odm_line('I_PTFAM_REASONMOTORIZED', q10areasonmotorized) 

    _odm_data = _odm_data + write_odm_line('I_PTFAM_REASONMOTORIZEDOTH', data_odk['q10areasonmotorizedo'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SAFEROUTESCHOOL', data_odk['q11routesafe'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SPORTCLUBFREQHRS', data_odk['q13sportclubshrs'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SPORTCLUBFREQMIN', data_odk['q13sportclubsmin'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BEDTIME', data_odk['q14bedtime'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WAKEUPTIME', data_odk['q15wakeuptime'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDSPLAYINGACTIVEH', data_odk['q16playoutwkdayshrs'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDSPLAYINGACTIVEM', data_odk['q16playoutwkdaysmins'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEPLAYINGACTIVEH', data_odk['q16playoutwkendshrs'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEPLAYINGACTIVEM', data_odk['q17playoutwkendsmins'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDREADINGH', data_odk['q17readingwkdayshrs'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDREADINGM', data_odk['q17readingwkdaysmins'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEREADINGH', data_odk['q17readingwkendhrs'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEREADINGM', data_odk['q16readingwkendmins'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDELECTRONICSH', data_odk['q18wdelectronicsh'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDELECTRONICSM', data_odk['q18wdelectronicsm'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEELECTRONICSH', data_odk['q18weelectronicsh'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEELECTRONICSM', data_odk['q18weelectronicsm'], is_integer = True)

    # data section 3
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BREAKFAST', data_odk['q19breakfast'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQFRUIT', data_odk['q20[FreshFruit]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQVEGETABLES', data_odk['q20[Vegetables]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQSOFTDRINKS', data_odk['q20[SoftDrinksSugar]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQCEREALS', data_odk['q20[Cereals]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQMEAT', data_odk['q20[Meat]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQFISH', data_odk['q20[Fish]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQEGG', data_odk['q20[Egg]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQLOWFATMILK', data_odk['q20[LowFatMilk]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQWHOLEFATMILK', data_odk['q20[WholeFatMilk]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQFLAVOUREDMILK', data_odk['q20[FlavouredMilk]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQCHEESE', data_odk['q20[Cheese]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQDAIRY', data_odk['q20[Dairy]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQFRUITJUICE', data_odk['q20[FruitJuice]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQDIET', data_odk['q20[DietSoftDrinks]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQCHIPS', data_odk['q20[Chips]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQCANDY', data_odk['q20[Candy]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQLEGUMES', data_odk['q20[Legumes]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PORTIONSFRUITVEG', data_odk['q19bportionsfruitveg'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HELPPREPARE', data_odk['q21ahelpprepare'], is_integer = True)

    q21ahelpprepareact = ''
    if (data_odk['q21ahelpprepareact[1]'] == 'Y'):
        q21ahelpprepareact = q21ahelpprepareact + '1,'
    if (data_odk['q21ahelpprepareact[2]'] == 'Y'):
        q21ahelpprepareact = q21ahelpprepareact + '2,'
    if (data_odk['q21ahelpprepareact[3]'] == 'Y'):
        q21ahelpprepareact = q21ahelpprepareact + '3,'
    if (data_odk['q21ahelpprepareact[4]'] == 'Y'):
        q21ahelpprepareact = q21ahelpprepareact + '4,'
    if (data_odk['q21ahelpprepareact[5]'] == 'Y'):
        q21ahelpprepareact = q21ahelpprepareact + '5,'
    if (data_odk['q21ahelpprepareact[6]'] == 'Y'):
        q21ahelpprepareact = q21ahelpprepareact + '6,'
    if (data_odk['q21ahelpprepareact[7]'] == 'Y'):
        q21ahelpprepareact = q21ahelpprepareact + '7,'
    if (q21ahelpprepareact != '' and q21ahelpprepareact[-1] ==','):
        q21ahelpprepareact = q21ahelpprepareact[0: (len(q21ahelpprepareact) -1)]
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HELPPREPACTIVITIES_2', q21ahelpprepareact) 

    _odm_data = _odm_data + write_odm_line('I_PTFAM_ORDERMEAL', data_odk['q21aordermeal'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEIGHTOPINION', data_odk['q21weightopinion'])

    # data section 4
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HOUSEHOLDBLOODPRESSURE', data_odk['q22househouldbloodpr'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HOUSEHOLDDIABETES', data_odk['q23householddiabetes'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HOUSEHOLDCHOLESTEROL', data_odk['q24householdcholeste'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SPOUSEAGE', data_odk['q25spousesage'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SPOUSEHEIGHT', data_odk['q25spouseheight'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SPOUSEWEIGHT', data_odk['q25spouseweight'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_YOUAGE', data_odk['q25youage'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_YOUHEIGHT', data_odk['q25youheight'], is_decimal = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_YOUWEIGHT', data_odk['q25youweight'], is_decimal = True)

    q26hmnr = ''
    if (data_odk['q26hmnr[Mother]'] == 'Y'):
        q26hmnr = q26hmnr + '1,'
    if (data_odk['q26hmnr[Father]'] == 'Y'):
        q26hmnr = q26hmnr + '2,'
    if (data_odk['q26hmnr[Stepmother]'] == 'Y'):
        q26hmnr = q26hmnr + '3,'
    if (data_odk['q26hmnr[Stepfather]'] == 'Y'):
        q26hmnr = q26hmnr + '4,'
    if (data_odk['q26hmnr[Grandfathers]'] == 'Y'):
        q26hmnr = q26hmnr + '5,'
    if (data_odk['q26hmnr[Grandmothers]'] == 'Y'):
        q26hmnr = q26hmnr + '6,'
    if (data_odk['q26hmnr[Else]'] == 'Y'):
        q26hmnr = q26hmnr + '7,'
    if (data_odk['q26hmnr[Foster]'] == 'Y'):
        q26hmnr = q26hmnr + '8,'
    if (q26hmnr != '' and q26hmnr[-1] ==','):
        q26hmnr = q26hmnr[0: (len(q26hmnr) -1)]
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HOMEADULTS', q26hmnr)

    _odm_data = _odm_data + write_odm_line('I_PTFAM_HOMEADULTSSPEC', data_odk['q26hmnrelsespec'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRBROTHER', data_odk['q26homebrother'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRSISTER', data_odk['q26homesister'], is_integer = True)

    # data section 5
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_CHILDBORN', data_odk['q27childborn'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_CHILDBORNOTH', data_odk['q27childbornoth'], is_utf8 = True)
    child_since = data_odk['q27achildlivingsince']
    if (child_since and len(child_since) == 4):
        child_since = '01/' + child_since
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_CHILDSINCE_2', child_since, is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_MOTHERBORN', data_odk['q28motherborn'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_MOTHERBORNOTH', data_odk['q28motherbornoth'], is_utf8 = True)
    mother_since = data_odk['q28amothersince']
    if (mother_since and len(mother_since) == 4):
        mother_since = '01/' + mother_since
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_MOTHERSINCE_2', mother_since, is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_FATHERBORN', data_odk['q29fatherborn'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_FATHERBORNOTH', data_odk['q29fatherbornoth'], is_utf8 = True)
    father_since = data_odk['q29afathersince']
    if (father_since and len(father_since) == 4):
        father_since = '01/' + father_since
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_FATHERSINCE_2', father_since, is_utf8 = True)
    # correct other langauage code
    if(data_odk['q30language'] and data_odk['q30language'] == '2'):
        q30language = '9'
    else:
        q30language = data_odk['q30language']
        
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_LANGUAGE', q30language)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_LANGUAGEOTH', data_odk['q30languageoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EDUYOU', data_odk['q31eduyou'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EDUSPOUSE', data_odk['q31eduspouse'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EARNINGS', data_odk['q32earnings'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPYOU', data_odk['q33occupyou'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPYOUOTH', data_odk['q33occupyouoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPSPOUSE', data_odk['q33occupspouse'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPSPOUSEOTH', data_odk['q33occupspouseoth'], is_utf8 = True)

    # data section 5
    q34monthsathome = ''
    if (data_odk['q34monthsathome[202003]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202003,'
    if (data_odk['q34monthsathome[202004]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202004,'
    if (data_odk['q34monthsathome[202005]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202005,'
    if (data_odk['q34monthsathome[202006]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202006,'
    if (data_odk['q34monthsathome[202007]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202007,'
    if (data_odk['q34monthsathome[202008]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202008,'
    if (data_odk['q34monthsathome[202009]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202009,'
    if (data_odk['q34monthsathome[202010]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202010,'
    if (data_odk['q34monthsathome[202011]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202011,'
    if (data_odk['q34monthsathome[202012]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202012,'
    if (data_odk['q34monthsathome[202101]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202101,'
    if (data_odk['q34monthsathome[202102]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202102,'
    if (data_odk['q34monthsathome[202103]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202103,'
    if (data_odk['q34monthsathome[202104]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202104,'
    if (data_odk['q34monthsathome[202105]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202105,'
    if (data_odk['q34monthsathome[202106]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202106,'
    if (data_odk['q34monthsathome[202107]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202107,'
    if (data_odk['q34monthsathome[202108]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202108,'
    if (data_odk['q34monthsathome[202109]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202109,'
    if (data_odk['q34monthsathome[202110]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202110,'
    if (data_odk['q34monthsathome[202111]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202111,'
    if (data_odk['q34monthsathome[202112]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202112,'
    if (data_odk['q34monthsathome[202201]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202201,'
    if (data_odk['q34monthsathome[202202]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202202,'
    if (data_odk['q34monthsathome[202203]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202203,'
    if (data_odk['q34monthsathome[202204]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202204,'
    if (data_odk['q34monthsathome[202205]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202205,'
    if (data_odk['q34monthsathome[202206]'] == 'Y'):
        q34monthsathome = q34monthsathome + '202206,'
    if (q34monthsathome != '' and q34monthsathome[-1] ==','):
        q34monthsathome = q34monthsathome[0: (len(q34monthsathome) -1)]
    _odm_data = _odm_data + write_odm_line('I_PTFAM_MONTHS_HOME', q34monthsathome) 

    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_INFECT_YOU_2', data_odk['q35infyou'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_INFECT_CHILD_2', data_odk['q35infchild'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_INFECT_SPOUSE_2', data_odk['q35infspouse'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_INFECT_OTHER_2', data_odk['q35infother'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_INFECT_OTHER_SPEC', data_odk['q35infspecify'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_CHANGE_FRUIT', data_odk['q36change[Fruit]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_CHANGE_VEGETABLES', data_odk['q36change[Vegetables]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_CHANGE_MEAT', data_odk['q36change[Meat]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_CHANGE_FISH', data_odk['q36change[Fish]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_CHANGE_DAIRY', data_odk['q36change[Dairy]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_CHANGE_CHIPS', data_odk['q36change[Chips]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_CHANGE_CANDY', data_odk['q36change[Candy]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_CHANGE_SOFTDRINKS', data_odk['q36change[SoftDrinks]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_CHANGE_CEREALS', data_odk['q36change[Cereals]'], is_integer = True)

    _odm_data = _odm_data + write_odm_line('I_PTFAM_ORDERMEAL_PRE', data_odk['q37orderpre'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ORDERMEAL_PAND', data_odk['q37orderduring'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BUY_LOCAL', data_odk['q38buy[Local]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BUY_SUPERMARKET', data_odk['q38buy[SuperMarket]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BUY_ONLINE', data_odk['q38buy[Online]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BUY_LARGE', data_odk['q38buy[LargeQuantities]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EAT_HOMEMADE', data_odk['q38buy[HomeMade]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EAT_PRECOOKED', data_odk['q38buy[PreCooked]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EAT_ORDERED', data_odk['q38buy[Ordered]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EAT_FAMILY', data_odk['q38buy[Family]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EAT_BREAKFAST', data_odk['q38buy[Breakfast]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_COOKING', data_odk['q38buy[Child]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SURPLUS', data_odk['q38buy[Surplus]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PLANNING', data_odk['q38buy[Planning]'], is_integer = True)

    # data section 6
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SLEEP_WD', data_odk['q39change[SleepWD]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SLEEP_WE', data_odk['q39change[SleepWE]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_LEARNING', data_odk['q39change[Learning]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ACTIVE_WD', data_odk['q39change[ActiveWD]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ACTIVE_WE', data_odk['q39change[ActiveWE]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ELECTRONICS_WD', data_odk['q39change[ElectronicsWD]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ELECTRONICS_WE', data_odk['q39change[ElectronicsWE]'], is_integer = True)

    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEIGHTOPINION_PRE', data_odk['q40weightpre'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEIGHTOPINION_PAND', data_odk['q40weightduring'], is_integer = True)

    _odm_data = _odm_data + write_odm_line('I_PTFAM_FIT_PRE', data_odk['q41feel1pre[Fit]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SCHL_PRE', data_odk['q41feel1pre[School]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ENERGY_PRE', data_odk['q41feel2pre[Energy]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SAD_PRE', data_odk['q41feel2pre[Sad]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ALONE_PRE', data_odk['q41feel2pre[Alone]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_TIME_PRE', data_odk['q41feel2pre[Time]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FRETIME_PRE', data_odk['q41feel2pre[FreeTime1]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FAIR_PRE', data_odk['q41feel2pre[Fair]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FRIENDS_PRE', data_odk['q41feel2pre[Friends]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ATTENTION_PRE', data_odk['q41feel2pre[Attention]'], is_integer = True)

    _odm_data = _odm_data + write_odm_line('I_PTFAM_FIT_PAND', data_odk['q41feel1pand[Fit]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SCHL_PAND', data_odk['q41feel1pand[School]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ENERGY_PAND', data_odk['q41feel2pand[Energy]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SAD_PAND', data_odk['q41feel2pand[Sad]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ALONE_PAND', data_odk['q41feel2pand[Alone]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_TIME_PAND', data_odk['q41feel2pand[Time]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FRETIME_PAND', data_odk['q41feel2pand[FreeTime1]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FAIR_PAND', data_odk['q41feel2pand[Fair]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FRIENDS_PAND', data_odk['q41feel2pand[Friends]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_ATTENTION_PAND', data_odk['q41feel2pand[Attention]'], is_integer = True)

    # data section 7
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPYOU_PRE', data_odk['q42occupyoupre'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPYOUOTH_PRE', data_odk['q42occyouothpre'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPSPOUSE_PRE', data_odk['q42occupspspre'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPSPOUSEOTH_PRE', data_odk['q42occspsothpre'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPYOU_PAND', data_odk['q42occupyoupand'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPYOUOTH_PAND', data_odk['q42occyouothpand'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPSPOUSE_PAND', data_odk['q42occupspspand'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPSPOUSEOTH_PAND', data_odk['q42occspsothpand'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EARNINGS_PRE', data_odk['q43earningspre'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EARNINGS_PAND', data_odk['q43earningspand'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SUPPORT', data_odk['q44support'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SUPPORT_SPECIFY', data_odk['q44supportspecify'], is_utf8 = True)

    # closing tags
    _odm_data = _odm_data + '          </ItemGroupData>'
    _odm_data = _odm_data + '        </FormData>'
    _odm_data = _odm_data + '      </StudyEventData>'
    _odm_data = _odm_data + '    </SubjectData>'
    _odm_data = _odm_data + '  </ClinicalData>'
    _odm_data = _odm_data + '</ODM>'

    return _odm_data
