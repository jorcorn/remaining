import math

import matplotlib.pyplot as plt

from .data import material_data, year_list, material_list_keys
# import pandas as pd
import matplotlib
from matplotlib.figure import Figure
import base64
from io import BytesIO


def material_op_temp_method(material):
    op_temp_calc = material_data[material]['Operating Temp Calculation']

    return op_temp_calc


def material_data_picker(material, stress_curve_choice):
    lmp_constant = material_data[material]['LMP_Value']
    is_op_temp_calculated = material_data[material]['Operating Temp Calculation']

    try:
        stress_data = material_data[material][stress_curve_choice]
    except:
        stress_data = material_data[material]['Stress - Avg']

    return lmp_constant, is_op_temp_calculated, stress_data



def oxide_growth(growth_method, tube_age, measured_scale, year_list,  ):
    return


def oxide_constant_calculator(steam_scale_thickness_mils, tube_age):
    k_constant = steam_scale_thickness_mils / math.sqrt(tube_age)

    return k_constant


def oxide_k_growth(tube_age, years_in_future, k_constant):
    new_scale = k_constant * math.sqrt(tube_age + years_in_future)

    return new_scale


def oxide_custom(measured_scale, growth_rate, years_in_future):
    new_scale = measured_scale + (years_in_future * growth_rate)

    return new_scale


def wastage_rate_calculator(thickest_wall, thinnest_wall, tube_age):
    total_wastage = thickest_wall - thinnest_wall
    # print("The wastage is: " + str(wastage))
    wastage_rate = total_wastage / tube_age
    # print("The wastage rate is: " + str(wastage_rate))
    return total_wastage, wastage_rate


def hoop_stress_calculator(system_pressure, od, wall_thickness, wastage_rate, years_in_future):
    # print((wall_thickness - (wastage_rate * years_in_future)))
    if (wall_thickness - (wastage_rate * years_in_future)) > 0:

        hoop_stress = (system_pressure * (od - (wall_thickness - (wastage_rate * years_in_future))) /
                                 (2 * (wall_thickness - (wastage_rate * years_in_future)))) / 1000


        hoop_stress = float("{:.10f}".format(hoop_stress))

    else:
        hoop_stress = 0

    # print("the hoop stress is: " + str(hoop_stress))
    return hoop_stress


def lmp_calculator(estimated_op_temp, tube_age, years_in_future, lmp):
    tube_age_hours = (tube_age + years_in_future) * 365 * 24 * 0.85
    lmp_value = ((estimated_op_temp + 460) * (lmp + math.log10(tube_age_hours + years_in_future)))
    lmp_value = float("{:.2f}".format(lmp_value))
    return lmp_value


def operating_temp_calculator(
        material,
        tube_age,
        years_in_future,
        lmp_constant,
        scale_thickness,
        calculate_op_temp,
        input_optemp=0
):
    if calculate_op_temp:
        if material == (material_list_keys[3] or material_list_keys[4]):
            multiplier = 0.000222
        else:
            multiplier = 0.00022
        operating_time_hours = (tube_age + years_in_future) * 365 * 24 * 0.85
        operating_temperature = (((math.log10(scale_thickness) + 7.25) /
                                  (multiplier * (lmp_constant + math.log10(operating_time_hours)))) - 460)
        return operating_temperature
    else:
        operating_temperature = input_optemp
        return operating_temperature


def fill(
        tube_age,
        init_oxide_thic,
        material_sel,
        thickest_wall,
        thinnest_wall,
        pressure,
        od,
        oxide_growth_method,
        stress_choice,
        custom_rate=0,
        eot=1000
):
    print(eot)
    lmp_constant, optemp_method_calc, curve = material_data_picker(material_sel, stress_choice)
    k = oxide_constant_calculator(init_oxide_thic, tube_age)
    w, wr = wastage_rate_calculator(thickest_wall, thinnest_wall, tube_age)

    if not optemp_method_calc:
        eot_microstructure = eot

    oxide_scale_thickness = [init_oxide_thic]
    eot_list, hoop_stress_list, lmp_list = []


    for year_in_future in year_list:

        # fills the oxide scale list based on the custom or constant selection
        if oxide_growth_method == 'custom':
            oxide_scale_thickness.append(oxide_custom(init_oxide_thic, custom_rate, year_in_future + 1))
        else:
            oxide_scale_thickness.append(oxide_k_growth(tube_age, year_in_future + 1, k))

        # fills the operating temperature list based on the selected method
        eot_list.append(operating_temp_calculator(material_sel, tube_age, year_in_future, lmp_constant,
                                                  oxide_scale_thickness[year_in_future], optemp_method_calc,
                                                  eot))

        # fills the hoop stress list and lmp data. Makes sure the data are positive values
        stress = hoop_stress_calculator(pressure, od, thinnest_wall, wr, year_in_future)

        if 40 > stress > 0:
            hoop_stress_list.append(stress)
            lmp_list.append(lmp_calculator(eot_list[year_in_future], tube_age, year_in_future, lmp_constant))

    return oxide_scale_thickness, eot_list, hoop_stress_list, lmp_list, curve


def comparison(hoop_stress_data_list, lmp_data_list, material_sel, curve):
    # print("The hoop stress data list: " + str(hoop_stress_data_list))
    est_lmp_list = material_data[material_sel]['LMP']
    est_stress_list = curve
    if hoop_stress_data_list != []:
        for index1, calc_stress_value in enumerate(hoop_stress_data_list):
            calc_lmp_value = lmp_data_list[index1]

            for index2, est_stress in enumerate(est_stress_list):
                est_lmp = est_lmp_list[index2]

                if (calc_stress_value > est_stress) and (calc_lmp_value > est_lmp):
                    # print("IT IS BIGGER AND WE PRINTED: ")
                    # print(calc_stress_value, est_stress_list[index2], calc_lmp_value, est_lmp_list[index2], index1)
                    return calc_stress_value, est_stress_list[index2], calc_lmp_value, est_lmp_list[index2], index1, True
        # print("I DIDN'T FIND ONE SO I PRINTED: ")
        # print(calc_stress_value, est_stress_list[index2], calc_lmp_value, est_lmp_list[index2], index1)
        return calc_stress_value, est_stress_list[index2], calc_lmp_value, est_lmp_list[index2], index1, False
    else:
        raise ValueError("Hoop stress field is empty")


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(material, lmp_data, hoop_stress_data, curve):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,5))
    plt.title('Larson-Miller Graphs')

    plt.plot(curve, material_data[material]['LMP'], 'o')
    plt.plot(hoop_stress_data, lmp_data, 'o')

    plt.xlabel('LMP, x 0.001')
    plt.ylabel('Stress, psi')
    plt.tight_layout()

    graph = get_graph()
    return graph
