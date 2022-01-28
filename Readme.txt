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

    1.driver订单不显示在my driven rides里面
    2.ride detail中不显示vehicle_type和licence
    3.可以接自己的订单，pickup会搜到自己的订单
    4.driver接单完把车辆信息改了怎么办
    5.是否发站内短信通知order cancel (email)
    6.timezone is incorrect(post date and time)
    7.Now __ people 应该用num_all