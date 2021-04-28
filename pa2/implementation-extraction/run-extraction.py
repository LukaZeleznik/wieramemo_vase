import sys,regexextraction,xpathextraction,automaticextraction

if(sys.argv[1] == "A"):
    regexextraction.main()
elif(sys.argv[1] == "B"):
    xpathextraction.main()
elif(sys.argv[1] == "C"):
    automaticextraction.main()