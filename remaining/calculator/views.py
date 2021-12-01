from django.shortcuts import render
from .forms import input_dataForm
from .models import input_data
from .functions import fill, comparison, get_plot, material_op_temp_method


# This connects to the raw html code that the website displays
# Gets called to the app's urls.py folder to connect to url

# TODO make it only display 'average curve' when only the average can be selected

# TODO: make it look pretty
# TODO: try to break everything
# TODO: put in reset and back buttons
# TODO: try and keep everything on one page

def calculator(request):
    year = None
    chart = None
    form = input_dataForm()
    if 'reset' in request.POST:
        if request.method == "POST":
            form = input_dataForm()
            return render(request, 'calculator/calculator.html', {
                'form': form,
            })

    if 'form button' in request.POST:
        method = None
        material_eot = None
        if request.method == "POST":
            form = input_dataForm(request.POST)
            method = None
            material_eot = None

            errors = form.errors.as_data
            print(errors)
            if form.is_valid():
                form.save()

                data = input_data.objects.last()
                method = data.oxide_method
                material_eot = material_op_temp_method(data.material)

                if (method == 'custom' and data.oxide_growth_rate == None) \
                        or (material_eot == False and data.est_op_temp == None):
                    pass

                else:

                    oxide_scale, eot_list, hoop_stress_list, lmp_list, curve = fill(data.tube_age,
                                                                                    data.measured_oxide_thickness,
                                                                                    data.material,
                                                                                    data.thickest_wall,
                                                                                    data.thinnest_wall,
                                                                                    data.pressure,
                                                                                    data.od,
                                                                                    data.oxide_method,
                                                                                    data.stress_curve,
                                                                                    data.oxide_growth_rate,
                                                                                    data.est_op_temp)

                    calc_stress, est_stress, calc_lmp, calc_est, year, boolean = \
                        comparison(hoop_stress_list, lmp_list, data.material, curve)

                    if year > 20:
                        year = 20

                    chart = get_plot(data.material, lmp_list, hoop_stress_list, curve)


        else:
            form = input_dataForm()

        return render(request, 'calculator/calculator.html', {'method': method,
                                                              'material_eot': material_eot,
                                                              'form': form,
                                                              'year': year,
                                                              'chart': chart,
                                                              })
    return render(request, 'calculator/calculator.html', {
        'form': form,
    })


def about(request):
    return render(request, 'calculator/about.html')
