from django import forms

from .models import input_data


MATERIAL_CHOICES = (
    ('T22 2.25Cr-1Mo', 'T22 2.25Cr-1Mo'),
    ('Carbon Steel', 'Carbon Steel'),
    ('TP 347H', 'TP 347H'),
    ('T1 Cr-Mo', 'T1 Cr-Mo'),
    ('T2 0.5Cr-0.5Mo', 'T2 0.5Cr-0.5Mo'),
    ('T12 1Cr-0.5Mo', 'T12 1Cr-0.5Mo'),
    ('T11 1.25Cr-0.5Mo', 'T11 1.25Cr-0.5Mo'),
    ('TP 321H', 'TP 321H'),
    ('TP 316H', 'TP 316H'),
    ('TP 304H', 'TP 304H'),
    ('T91 Cr-Mo-V', 'T91 Cr-Mo-V'),
    ('T5 5Cr-0.5Mo', 'T5 5Cr-0.5Mo'),
)

OXIDE_METHOD_CHOICES = (
    ('equation', 'Parabolic'),
    ('custom', 'Customized'),
)

LMP_CURVE_CHOICES = (
('Stress - Avg', 'Average of Minimum and Mean'),
    ('Stress - Min', 'Minimum'),
    ('Stress - Max', 'Mean'),
)


class input_dataForm(forms.ModelForm):

    class Meta:
        model = input_data
        fields = ['material', 'pressure', 'od', 'min_wall_thickness',
                  'tube_age', 'measured_oxide_thickness', 'thickest_wall',
                  'thinnest_wall', 'oxide_method', 'stress_curve', 'oxide_growth_rate',
                  'est_op_temp', 'key']


    material = forms.ChoiceField(widget=forms.Select(attrs={'class': 'myfieldclass2'}), choices=MATERIAL_CHOICES)
    pressure = forms.FloatField(widget=forms.NumberInput(attrs={'size': 8, 'class': 'myfieldclass'}))
    od = forms.FloatField(widget=forms.NumberInput(attrs={'size': 8, 'class': 'myfieldclass'}))
    min_wall_thickness = forms.FloatField(widget=forms.NumberInput(attrs={'size': 8, 'class': 'myfieldclass'}))
    tube_age = forms.FloatField(widget=forms.NumberInput(attrs={'size': 8, 'class': 'myfieldclass'}))
    measured_oxide_thickness = forms.FloatField(widget=forms.NumberInput(attrs={'size': 8, 'class': 'myfieldclass'}))
    thickest_wall = forms.FloatField(widget=forms.NumberInput(attrs={'size': 8, 'class': 'myfieldclass'}))
    thinnest_wall = forms.FloatField(widget=forms.NumberInput(attrs={'size': 8, 'class': 'myfieldclass'}))
    oxide_method = forms.ChoiceField(widget=forms.Select(attrs={'title': 'Oxide Growth Method', 'class': 'myfieldclass2'}), choices=OXIDE_METHOD_CHOICES)
    stress_curve = forms.ChoiceField(widget=forms.Select(attrs={'width': 50, 'class': 'myfieldclass2'}), choices=LMP_CURVE_CHOICES)
    oxide_growth_rate = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'size': 8, 'class': 'myfieldclass'}))
    est_op_temp = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'size': 8, 'class': 'myfieldclass'}))
    key = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'size': 8, 'class': 'myfieldclass'}))




    def clean_pressure(self, *args, **kwargs):
        pressure = self.cleaned_data.get('pressure')
        if pressure > 0:
            return pressure
        else:
            raise forms.ValidationError("This is not a valid pressure")

    def clean_measured_oxide_thickness(self, *args, **kwargs):
        measured_oxide_thickness = self.cleaned_data.get('measured_oxide_thickness')
        if measured_oxide_thickness > 0:
            return measured_oxide_thickness
        else:
            raise forms.ValidationError("This is not a valid oxide thickness")

    def clean_oxide_growth_rate(self, *args, **kwargs):
        oxide_growth_rate = self.cleaned_data.get('oxide_growth_rate')
        if oxide_growth_rate == None:
            return oxide_growth_rate
        elif oxide_growth_rate > 0:
            return oxide_growth_rate
        else:
            raise forms.ValidationError("This is not a valid oxide growth rate")

    def clean_est_op_temp(self, *args, **kwargs):
        est_op_temp = self.cleaned_data.get('est_op_temp')
        if est_op_temp == None:
            return est_op_temp
        elif est_op_temp > 0:
            return est_op_temp
        else:
            raise forms.ValidationError("This is not a valid oxide growth rate")

    def clean_od(self, *args, **kwargs):
        od = self.cleaned_data.get('od')
        if od > 0:
            return od
        else:
            raise forms.ValidationError("Make sure your outside diameter is positive")

    def clean_thickest_wall(self, *args, **kwargs):
        thickest_wall = self.cleaned_data.get('thickest_wall')
        if thickest_wall > 0:
            return thickest_wall
        else:
            raise forms.ValidationError("Make sure your thickest wall is positive")

    def clean_thinnest_wall(self, *args, **kwargs):
        thinnest_wall = self.cleaned_data.get('thinnest_wall')
        if thinnest_wall > 0:
            return thinnest_wall
        else:
            raise forms.ValidationError("Make sure your thinnest wall is positive")


    def clean_tube_age(self, *args, **kwargs):
        tube_age = self.cleaned_data.get('tube_age')
        if tube_age > 0:
            return tube_age
        else:
            raise forms.ValidationError("Tube age must be greater than 0")

    def clean_key(self, *args, **kwargs):
        key = self.cleaned_data.get('key')
        if key == 7007:
            return key
        else:
            raise forms.ValidationError("Incorrect key")

    def clean(self):

        cleaned_data = super().clean()
        thickest_wall = cleaned_data.get('thickest_wall')
        thinnest_wall = cleaned_data.get('thinnest_wall')
        od = cleaned_data.get('od')

        if thickest_wall and thinnest_wall and od:
            if od > thickest_wall > thinnest_wall:
                return self.cleaned_data
            else:
                raise forms.ValidationError("Make sure:  Outside Diameter  >  Thickest Wall  >  Thinnest Wall")

