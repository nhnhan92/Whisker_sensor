import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import math as m



# Định nghĩa các tham số của đường xoắn ốc
r = 13     # bán kính của đường xoắn ốc ở mặt phẳng đáy
p = 2       # chiều cao của đường xoắn ốc
h = 139.7682521    # chiều cao của đường xoắn ốc (khoảng cách từ điểm đầu đến điểm cuối)

# Tính toán số điểm trên đường xoắn ốc
N = 2000
idx_z_limit = int(24*N/h)
# Tính toán tọa độ của các điểm trên đường xoắn ốc
z = np.linspace(0, h, N)

x = ((h-z)/h)*r*np.cos((2*np.pi)*z/p+np.pi)
y = ((h-z)/h)*r*np.sin((2*np.pi)*z/p+np.pi)

z2 = np.linspace(0, h, N)

x2 = -((h-z2)/h)*r*np.cos(-(2*np.pi)*z2/p-np.pi)
y2 = -((h-z2)/h)*r*np.sin(-(2*np.pi)*z2/p-np.pi)

# Save node information
for i in range(1,3):
	filePath_node = os.getcwd()+"/fiber"+str(i)+"_info.csv"
	try:
		os.remove(filePath_node)
	except:
		print("Error while deleting file ", filePath_node)
	header = ["Fiber "+ str(i)+": Spring Idx", "x (mm)", "y (mm)", "z (mm)"]
	with open(filePath_node, "w", newline="") as file_open:
		writer = csv.writer(file_open, delimiter=",")
		writer.writerow(header)
		for j in range(idx_z_limit):
			if i == 1:
				writer.writerow([j,x[j],y[j],z[j]])
			else:
				writer.writerow([j,x2[j],y2[j],z2[j]])


# Vẽ đường xoắn ốc
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot(x, y, z, label='fiber 1')
ax.plot(x2, y2, z2, label='fiber 2')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_zlim([0, 24])
ax.legend()
plt.show()
