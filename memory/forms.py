from django import forms
from django.contrib.auth.models import User
# from django.contrib.admin.widgets import AdminDateWidget
from .models import Account, Memory, Geo, MemoryImage
import json
from bootstrap_datepicker_plus.widgets import DatePickerInput


class AccountForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(), label="パスワード")

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username', 'email', 'password')
        labels = {'username': 'ニックネーム'}

        username = forms.CharField(
            widget=forms.Textarea(
            attrs={
                'placeholder': 'ユーザー名',
            }
        )
        )


class AddAccountForm(forms.ModelForm):
    class Meta():

        model = Account
        fields = ('image', 'birthplace')
        labels = {'image': 'プロフィール画像', 'birthplace': '出身地'}


#jsonファイル読み込み
def readJson(filename):
        with open(filename, 'r',encoding="utf-8_sig") as fp:
            return json.load(fp)

def get_prefecture():
    """ 都道府県を選択する """
    filepath = './static/memory/prefecture.json'
    all_data = readJson(filepath)
    prefectures = list(all_data.keys())
    all_prefectures = [('-----', '---都道府県の選択---')]
    for prefecture in prefectures:
        all_prefectures.append((prefecture, prefecture))
    all_prefectures.append(('海外','海外'))
    return all_prefectures
 

#地図フォーム
class GeoForm(forms.ModelForm):

    class Meta:
        model = Geo
        fields = ('ken', 'lat','lng',)
    
    lat = forms.DecimalField(
        required=True,
        label='緯度',
        widget=forms.TextInput(
            attrs={
                'placeholder': '緯度',
                'id': 'lat',
                

            }
        ))
    
    lng = forms.DecimalField(
        required=True,
        label='経度',
        widget=forms.TextInput(
            attrs={
                'placeholder': '経度',
                'id': 'lng',
                'opacity': '0',
            }
        ))
    ken = forms.ChoiceField(
        choices= get_prefecture(),
        required= True,
        label='都道府県'
    )

#思い出記録フォーム
class PostForm(forms.ModelForm):

    class Meta:
        model = Memory
        fields = ('date',
                  'memory_image', 'weather', 'feeling','place')
    date = forms.DateField(
        label='旅行日',
        widget=DatePickerInput(format='%Y-%m-%d')
    )

    memory_image = forms.ImageField(
    widget=forms.ClearableFileInput(attrs={'multiple': True}),
    label='旅行画像',
    required=False,
    )

    weather = forms.fields.ChoiceField(
        choices=(
            ('晴れ', '晴れ'),
            ('雨', '雨'),
            ('曇り', '曇り'),
            ('雪', '雪'),
            ('台風', '台風'),
        ),
        required=True,
        widget=forms.widgets.Select(),
        label='天気'
    )

    feeling = forms.CharField(
        required=False,
        max_length=1200,
        label='感想',
        widget=forms.Textarea(
            attrs={
                'placeholder': '感想を記述してください',
                'cols':60,
                'rows':7,
            }
        )
    )


class MemoryImageForm(forms.ModelForm):

    class Meta:
        model = MemoryImage
        fields = ["memory","image"]