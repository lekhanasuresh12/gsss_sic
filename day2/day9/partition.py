def partition_array(my_list):
    pivot = my_list[-1]
    j=0
    for i in range(len(my_list)-1):
        if pivot > my_list[i]:
            my_list[i], my_list[j] = my_list[j], my_list[i]
            j+=1
            my_list[0], my_list[j] = my_list[j], my_list[0]

            l1=[34,223,22,31,1,100,50,40,22,72]
            print(f'before partition: {11}')
            partition_array(11)
            print(f'after partition:{11}')
            