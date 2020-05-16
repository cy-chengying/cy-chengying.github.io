from django import forms

# 表单类用以生成表单
class AddForm(forms.Form):
    # name = forms.CharField()
    headimg = forms.FileField()

class PriceForm(forms.Form):
    item_type = (
        ('book','书本类'),
        ('res','物品类'),
        ('necessary','日用品类'),
        ('other','其他'),
    )
    salemoney = forms.FloatField(label='金额',max_value=250 ,widget=forms.TextInput(attrs = {'class':'form-control'}))
    email = forms.EmailField(label="邮箱地址",max_length=250 , widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sort = forms.ChoiceField(label='物品种类',choices=item_type)