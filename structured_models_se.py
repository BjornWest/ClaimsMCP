"""
Pydantic-modeller för strukturerad output i Claimify-pipelinen.
Dessa modeller definierar förväntat svarsformat för varje steg.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class UrvalsSvar(BaseModel):
    """Svarsmodell för Urvals-stadiet (Selection)."""

    språk: str = Field(description="Språket som meningen är skriven på. Detta språk måste resten av svaret använda för att beskriva meningen.")
    
    mening: str = Field(description="Originalmeningen som analyseras. VIKTIGT: Återge meningen ord för ord som den är skriven.")
    
    tankeprocess: str = Field(
        description="4-stegs -tankeprocess (beskrivs ovan) som analyserar meningen"
    )
    
    slutlig_bedömning: Literal["Innehåller ett specifikt och verifierbart påstående", "Innehåller INTE ett specifikt och verifierbart påstående"] = Field(
        description="Huruvida meningen innehåller ett specifikt och verifierbart påstående"
    )
    
    mening_med_endast_verifierbar_info: Optional[str] = Field(
        description="Meningen med endast verifierbar information, 'förblir oförändrad' om inga ändringar behövs, eller None om inget verifierbart påstående finns",
        default=None
    )


class AvtydningsSvar(BaseModel):
    """Svarsmodell för Avtydnings-stadiet (Disambiguation)."""
    
    ofullstandiga_namn_akronymer_förkortningar: str = Field(
        description="Analys av partiella namn och odefinierade akronymer/förkortningar i meningen"
    )
    
    språklig_tvetydighetsanalys: str = Field(
        description="Steg-för-steg-analys av referentiell och strukturell tvetydighet i meningen"
    )
    
    krävda_ändringar: Optional[str] = Field(
        description="Lista över ändringar som krävs för att avkontextualisera meningen, eller None om den inte kan avkontextualiseras",
        default=None
    )
    
    avkontextualiserad_mening: Optional[str] = Field(
        description="Den slutgiltiga avkontextualiserade meningen, eller 'Kan inte avkontextualiseras' om tvetydighet inte kan lösas",
        default=None
    )


class Påstaende(BaseModel):
    """Ett enskilt faktapåstående med verifieringsegenskaper."""
    
    text: str = Field(description="Påståendetexten med essentiell kontext/förtydliganden inom parentes")
    
    verifierbar: bool = Field(
        description="Alltid True - indikerar att detta påstående kan faktagranskas som sant eller falskt",
        default=True
    )


class DekomponeringsSvar(BaseModel):
    """Svarsmodell för Dekomponerings-stadiet (Decomposition)."""

    språk: str = Field(description="Språket som meningen är skriven på. Detta språk måste resten av svaret använda för att beskriva meningen.")
    
    mening: str = Field(description="Meningen som dekomponeras. VIKTIGT: Återge meningen ord för ord som den är skriven.")
    
    referentiella_termer: Optional[str] = Field(
        description="Översikt över referentiella termer vars referenter måste förtydligas, eller 'Inga' om inga referentiella termer finns",
        default=None
    )
    
    maximalt_förtydligad_mening: str = Field(
        description="Mening som artikulerar diskreta informationsenheter och förtydligar referenter"
    )
    
    propositionsintervall: str = Field(
        description="Intervallet för möjligt antal propositioner (t.ex. '3-5')"
    )
    
    propositioner: List[str] = Field(
        description="Lista över specifika, verifierbara och avkontextualiserade propositioner"
    )
    
    slutgiltiga_påstaenden: List[Påstaende] = Field(
        description="Slutgiltig lista av påståenden med text och verifierbar egenskap (alltid True) för att vägleda LLM:ens tänkande kring faktagranskning"
    )