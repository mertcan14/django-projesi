from django import forms
from game.models import Oyunlar
class addGameForm(forms.ModelForm):
    class Meta:
        model=Oyunlar
        fields=["oyun_isim","bilgisayar_platform","mobil_platform","konsol_platform","kategoriler","geliştirici","cıkıs_tarih","türkce_dil","hakkında","game_image"]