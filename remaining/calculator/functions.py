import math

import matplotlib.pyplot as plt

from .data import material_data, year_list, material_list_keys
import base64
from io import BytesIO


# material = 'T22 2.25Cr-1Mo'

def material_op_temp_method(selected_material):
    op_temp_method = material_data[selected_material]['Operating Temp Calculation']

    return op_temp_method


def material_data_picker(selected_material, stress_choice):
    lmp_value = material_data[selected_material]['LMP_Value']
    op_temp_method = material_data[selected_material]['Operating Temp Calculation']

    try:
        curve = material_data[selected_material][stress_choice]
    except:
        curve = material_data[selected_material]['Stress - Avg']
    return lmp_value, op_temp_method, curve


def oxide_constant_calculator(steam_scale_thickness_mils, tube_age):
    k = steam_scale_thickness_mils / math.sqrt(tube_age)

    return k


def oxide_k_growth(tube_age, years_in_future, k_constant):
    new_scale = k_constant * math.sqrt(tube_age + years_in_future)

    return new_scale


def oxide_custom(measured_scale, growth_rate, years_in_future):
    new_scale = measured_scale + (years_in_future * growth_rate)

    return new_scale


def wastage_rate_calculator(thickest_wall, thinnest_wall, tube_age):
    wastage = thickest_wall - thinnest_wall
    # print("The wastage is: " + str(wastage))
    wastage_rate = wastage / tube_age
    # print("The wastage rate is: " + str(wastage_rate))
    return wastage, wastage_rate


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


def lmp_calculator(estimated_optemp, tube_age, years_in_future, lmp):
    tube_age_hours = (tube_age + years_in_future) * 365 * 24 * 0.85
    lmp_value = ((estimated_optemp + 460) * (lmp + math.log10(tube_age_hours + years_in_future)))
    lmp_value = float("{:.2f}".format(lmp_value))
    return lmp_value


def operating_temp_calculator(
        material,
        tube_age,
        years_in_future,
        lmp,
        steam_scale_thickness_mils,
        calculation_method,
        input_optemp=0
):
    if calculation_method:
        if material == (material_list_keys[3] or material_list_keys[4]):
            multiplier = 0.000222
        else:
            multiplier = 0.00022
        operating_time_hours = (tube_age + years_in_future) * 365 * 24 * 0.85
        operating_temperature = (((math.log10(steam_scale_thickness_mils) + 7.25) /
                                  (multiplier * (lmp + math.log10(operating_time_hours)))) - 460)
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
    larson_miller, optemp_method_calc, curve = material_data_picker(material_sel, stress_choice)
    k = oxide_constant_calculator(init_oxide_thic, tube_age)
    w, wr = wastage_rate_calculator(thickest_wall, thinnest_wall, tube_age)


    oxide_scale_thickness = [init_oxide_thic]

    eot_list = []
    hoop_stress_list = []
    lmp_list = []

    for year_in_future in year_list:

        # fills the oxide scale list based on the custom or constant selection
        if oxide_growth_method == 'custom':
            oxide_scale_thickness.append(oxide_custom(init_oxide_thic, custom_rate, year_in_future + 1))
        else:
            oxide_scale_thickness.append(oxide_k_growth(tube_age, year_in_future + 1, k))

        # fills the operating temperature list based on the selected method
        eot_list.append(operating_temp_calculator(material_sel, tube_age, year_in_future, larson_miller,
                                                  oxide_scale_thickness[year_in_future], optemp_method_calc,
                                                  eot))

        # fills the hoop stress list and lmp data. Makes sure the data are positive values
        stress = hoop_stress_calculator(pressure, od, thinnest_wall, wr, year_in_future)

        if stress > 0:
            hoop_stress_list.append(stress)
            lmp_list.append(lmp_calculator(eot_list[year_in_future], tube_age, year_in_future, larson_miller))

    return oxide_scale_thickness, eot_list, hoop_stress_list, lmp_list, curve


def comparison(hoop_stress_data_list, lmp_data_list, material_sel, curve):
    # print("The hoop stress data list: " + str(hoop_stress_data_list))
    est_lmp_list = material_data[material_sel]['LMP']
    est_stress_list = curve
    if hoop_stress_data_list != []:
        calc_stress_value = None
        index2 = None
        calc_lmp_value = None
        index1 = 0
        for index1, calc_stress_value in enumerate(hoop_stress_data_list):
            calc_lmp_value = lmp_data_list[index1]

            for index2, est_stress in enumerate(est_stress_list):
                est_lmp = est_lmp_list[index2]

                if (calc_stress_value > est_stress) and (calc_lmp_value > est_lmp):
                    # print("IT IS BIGGER AND WE PRINTED: ")
                    # print(calc_stress_value, est_stress_list[index2], calc_lmp_value, est_lmp_list[index2], index1)
                    print("Index1 is: " + str(index1))
                    return calc_stress_value, est_stress_list[index2], calc_lmp_value, est_lmp_list[
                        index2], index1, True
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
    plt.figure(figsize=(8, 8))
    plt.figure(facecolor='#E9E9E9')
    plt.title('Larson-Miller Graph')

    plt.plot(material_data[material]['LMP'], curve, 'o', color='xkcd:red', markersize=4)
    plt.plot(lmp_data, hoop_stress_data, 'o', color='xkcd:blue', markersize=4)

    plt.xlabel('LMP * 0.001')
    plt.ylabel('Stress, psi')
    plt.legend(['Larson-Miller Curve', 'Calculated Data'])

    ax = plt.gca()
    ax.set_facecolor('#E9E9E9')
    ax.set_alpha(1.0)
    plt.tight_layout()
    plt.rcParams.update({'font.size': 14})
    graph = get_graph()
    return graph
