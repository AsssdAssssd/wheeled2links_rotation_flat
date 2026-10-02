import time
import math

import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("assets/wheel_leg_car_2links/wheel_leg_car_2link.xml")
data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()

        mujoco.mj_step(model, data)

		# 隔一秒显示一次接触点
        with viewer.lock():#防止查看器出现竞争
            viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = int(data.time % 2)

        viewer.sync()#定时刷新，推送gui，主要的还是让修改快速生效和step对其，但是由于查看器本身就有个后台渲染县城，看起来差不多

        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)
