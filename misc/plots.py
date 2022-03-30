import matplotlib.pyplot as plt

def explocalc(br1, br2, v):
    return (br1+br2-2*v)/2
# LeducA
# iterations1 5000 iterations2 1000 sgdepth 4 depththreshold 6
abstractions = [1,0.95,0.9,0.75,0.5]
bpbr1 = [1.34622, 1.34197, 1.35285,1.502197, 1.5083]
bpbr2 = [-1.28018, -1.29306, -1.4509 ,-1.33475,-1.509972]
sgbr1 = [1.28416,1.23069,1.21334,1.37468,1.1268734]
sgbr2 = [-1.29700,-1.29083,-1.30849,-1.379270, -1.29462]
bpv = [-0.06266,-0.122989,-0.21564,-0.131286,-0.2343]
sgv = [-0.03992,-0.114626,-0.138690,-0.097768,-0.2987]

bpexp = []
for i in range(5):
    bpexp.append(explocalc(bpbr1[i], bpbr2[i], bpv[i]))

sgexp = []
for i in range(5):
    sgexp.append(explocalc(sgbr1[i], sgbr2[i], sgv[i]))

plt.figure(0)
plt.plot(abstractions,bpexp)
plt.xlabel('Portion of Information Sets')
plt.ylabel('Exploitability*')
plt.title('LeducA: Abstraction vs Exploitability in blueprint')
plt.show()

plt.figure(1)
plt.plot(abstractions,sgexp)
plt.xlabel('Portion of Information Sets')
plt.ylabel('Exploitability*')
plt.title('LeducA: Abstraction vs Exploitability in refined')
plt.show()

plt.figure(2)
plt.plot(abstractions,bpexp)
plt.plot(abstractions,sgexp)
plt.xlabel('Portion of Information Sets')
plt.ylabel('Exploitability*')
plt.title('LeducA: blueprint vs refined')
plt.show()

#leduc9
bpbr1 = 1.74399
bpbr2 = -1.3534
bpv   = 0.24431

sgbr1 = 1.744399774270526 # dt 6 d 4
sgbr2 = -1.3289918511299996
sgv   = 0.2457255297954959

print(explocalc(bpbr1, bpbr2, bpv), explocalc(sgbr1, sgbr2, sgv))

#1.7551648045241801 -1.4387611742769992 0.2233713388781312
#1.7721241407062696 -1.3473863423435983 0.24933366977655216 d 2 dt 8
#1.744399774270526 -1.3289918511299996 0.2457255297954959 d 1 dt 8
#1.744399774270526 -1.363170619474277 0.24628510283146868 d1 dt 7
