Status now:
    1. forms --> views
    2. blog --> ride
    3. Post --> request

    1/27
    Add num_all, is_open fields in Ride model
    Match special requests?

    1/28
    Now the username is clickable, however we don't have a profile view for other users
    urls里面用ride_id会冲突吗
    Forgot to write order.save(), after modifying driver information, the updates haven't been posted

    1.driver订单不显示在my driven rides里面 --> forgot order.save(),did not save the driver after accepting order
    2.ride detail中不显示vehicle_type和licence --> driver.driverinfo.vehicle_type, field is under driverinfo module, not user
    3.可以接自己的订单，pickup会搜到自己的订单 --> if(ride.owner!=user)
    
    4.driver接单完把车辆信息改了怎么办
    5.是否发email通知order cancel (email)
    6.timezone is incorrect(post date and time)
    7.Now __ people 应该用num_all

    8.Once the order is completed, we should restrict the user from editing it or completing it again --> UpdateView -> test_func -> if (ride.complete==False)
    9.When the user hasn't specified a vehicle type, all type should match --> Q(vehicle_type=request.user.driverinfo.vehicle_type)|Q(vehicle_type='')
    
    10.Search results中的order用时间排序