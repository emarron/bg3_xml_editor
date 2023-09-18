import xml.etree.ElementTree as ET

# changes material shader from various VT versions
# here be the dictionary
'''
CHAR_AlphaBlend_GM_Udim_Flowmap.lsx
CHAR_ARM_Fur_HairShading.lsx
CHAR_BASE.lsx
CHAR_BASE_2S_GM_VT.lsx
CHAR_BASE_2S_VertCut_VT.lsx
CHAR_BASE_2S_VT.lsx
CHAR_BASE_AlphaBlend_2S.lsx
CHAR_BASE_AlphaTest.lsx
CHAR_BASE_AlphaTest_2S.lsx
CHAR_BASE_AlphaTest_2S_Anisotropy_MSK_VT.lsx
CHAR_BASE_AlphaTest_2S_BGM_GM_VT.lsx
CHAR_BASE_AlphaTest_2s_ClothModel_VT.lsx
CHAR_BASE_AlphaTest_2S_Dither.lsx
CHAR_BASE_AlphaTest_2S_Dither_Anisotropy_MSKA_VT.lsx
CHAR_BASE_AlphaTest_2S_Dither_Anisotropy_VT.lsx
CHAR_BASE_AlphaTest_2S_Dither_MSK_VT.lsx
CHAR_BASE_AlphaTest_2S_GM_MSK_VT.lsx
CHAR_BASE_AlphaTest_2S_MSK_VT.lsx
CHAR_BASE_Alphatest_2S_VertCut_MSK_VT.lsx
CHAR_BASE_AlphaTest_2S_VertCut_VT.lsx
CHAR_BASE_AlphaTest_2S_VT.lsx
CHAR_BASE_AlphaTest_BGM_GM_VT.lsx
CHAR_BASE_AlphaTest_ClothModel_VertCut_VT.lsx
CHAR_BASE_AlphaTest_ClothModel_VT.lsx
CHAR_BASE_AlphaTest_Dither_MSK_VT.lsx
CHAR_BASE_AlphaTest_Flowmap_GM_VT.lsx
CHAR_BASE_AlphaTest_GM_MSK_VT.lsx
CHAR_BASE_AlphaTest_GM_VT.lsx
CHAR_BASE_AlphaTest_MSK_VT.lsx
CHAR_BASE_AlphaTest_VertCut_GM_MSK_VT.lsx
CHAR_BASE_AlphaTest_VertCut_VT.lsx
CHAR_BASE_AlphaTest_VT.lsx
CHAR_BASE_Bloody_NoColor_VT.lsx
CHAR_BASE_ClothModel_Pearlescence_VT.lsx
CHAR_BASE_ClothModel_VertCut_VT.lsx
CHAR_BASE_ClothModel_VT.lsx
CHAR_Base_Distort_GM_VC_SSS_Detail_VT.lsx
CHAR_Base_Distort_GM_VC_SSS_VT.lsx
CHAR_Base_Distort_GM_VC_VT.lsx
CHAR_BASE_GM.lsx
CHAR_BASE_GMPulse_VT.lsx
CHAR_BASE_GM_MSK.lsx
CHAR_BASE_GM_MSK_VertCut_VT.lsx
CHAR_BASE_GM_SSS.lsx
CHAR_BASE_GM_SSS_VT.lsx
CHAR_BASE_GM_VT.lsx
CHAR_BASE_MSK_VertCut_VT.lsx
CHAR_BASE_MSK_VT.lsx
CHAR_BASE_MSK_WM.lsx
CHAR_BASE_Pearlescence_AlphaTest_MSK_VT.lsx
CHAR_BASE_Pearlescence_GMPulse_VT.lsx
CHAR_BASE_Pearlescence_VT.lsx
CHAR_BASE_SSS.lsx
CHAR_BASE_SSS_2S_MSK_VT.lsx
CHAR_BASE_SSS_AlphaTested_2S_MSK_VT.lsx
CHAR_BASE_SSS_AlphaTested_GM_VT.lsx
CHAR_BASE_SSS_AlphaTested_MSK.lsx
CHAR_BASE_SSS_AlphaTested_VT.lsx
CHAR_BASE_SSS_BGM_MSK.lsx
CHAR_Base_SSS_BrokenTeeth_VT.lsx
CHAR_Base_SSS_ExtraOcclusion_VT.lsx
CHAR_BASE_SSS_Fresnel.lsx
CHAR_BASE_SSS_GM_MSK.lsx
CHAR_BASE_SSS_GM_MSK_DetailMap.lsx
CHAR_BASE_SSS_GM_VertCut_DetailMap_VT.lsx
CHAR_BASE_SSS_MSK_WM.lsx
CHAR_BASE_SSS_VertCut.lsx
CHAR_BASE_SSS_VertCut_VT.lsx
CHAR_BASE_SSS_VT.lsx
CHAR_BASE_SSS_WM.lsx
CHAR_BASE_VertCut.lsx
CHAR_BASE_VertCut_VT.lsx
CHAR_BASE_VT.lsx
CHAR_BASE_WM.lsx
CHAR_Eye_Fiery_FX.lsx
CHAR_Eye_Parallax.lsx
CHAR_Eye_Parallax_Creature.lsx
CHAR_Eye_Parallax_Creature_FX.lsx
CHAR_Eye_Parallax_FX.lsx
CHAR_Eye_Parallax_Magical_FX.lsx
CHAR_Feathers_Bloody.lsx
CHAR_Fur.lsx
CHAR_Fur_HairShading_MSK1.lsx
CHAR_Fur_IDmsk.lsx
CHAR_Glass_PixelLighting.lsx
CHAR_GM_Fresnel.lsx
CHAR_Hair.lsx
CHAR_Hair_BodyInfluence.lsx
CHAR_Hair_ExtraUV.lsx
CHAR_Mannequin.lsx
CHAR_Pulse.lsx
CHAR_ScryingEye_Core.lsx
CHAR_ScryingEye_Pupil.lsx
CHAR_Shadow_Body.lsx
CHAR_Shadow_Shadow.lsx
'''
# some determination is made to find correct version
# vt types
CHAR_BASE_AlphaTest_2S_type = ['CHAR_BASE_AlphaTest_2S_Anisotropy_MSK_VT', 'CHAR_BASE_AlphaTest_2s_ClothModel_VT',
                               'CHAR_BASE_AlphaTest_2S_MSK_VT', 'CHAR_BASE_Alphatest_2S_VertCut_MSK_VT',
                               'CHAR_BASE_AlphaTest_2S_VertCut_VT', 'CHAR_BASE_AlphaTest_2S_VT']
# we cannot change anything with alpha + GM
CHAR_BASE_AlphaTest_2S_dither_type = ['CHAR_BASE_AlphaTest_2S_Dither_Anisotropy_MSKA_VT',
                                      'CHAR_BASE_AlphaTest_2S_Dither_Anisotropy_VT',
                                      'CHAR_BASE_AlphaTest_2S_Dither_MSK_VT']
CHAR_BASE_AlphaTest_type = ['CHAR_BASE_AlphaTest_ClothModel_VertCut_VT',
                            'CHAR_BASE_AlphaTest_ClothModel_VT', 'CHAR_BASE_AlphaTest_Dither_MSK_VT',
                            'CHAR_BASE_AlphaTest_MSK_VT', 'CHAR_BASE_AlphaTest_VertCut_VT', 'CHAR_BASE_AlphaTest_VT']
CHAR_BASE_ClothModel_type = ['CHAR_BASE_ClothModel_Pearlescence_VT', 'CHAR_BASE_ClothModel_VertCut_VT',
                             'CHAR_BASE_ClothModel_VT']
CHAR_BASE_2S_type = ['CHAR_BASE_2S_VertCut_VT', 'CHAR_BASE_2S_VT']
CHAR_BASE_VertCut_type = ['CHAR_BASE_VertCut_VT']
CHAR_BASE_GM_type = ['CHAR_BASE_GM_VT']
CHAR_BASE_GM_MSK_type = ['CHAR_BASE_GM_MSK_VertCut_VT']
CHAR_BASE_GM_SSS_type = ['CHAR_BASE_GM_SSS_VT']
CHAR_BASE_MSK_type = ['CHAR_BASE_MSK_VertCut_VT', 'CHAR_BASE_MSK_VT']
CHAR_BASE_type = ['CHAR_BASE_VT']  # only do this manually, probably.
# these are the only ones I feel comfortable doing automatically


mat_tree = ET.parse('material.xml')
mat_root = mat_tree.getroot()
sourcefile_attributes = mat_root.findall(".//attribute[@id='SourceFile']")
# massive pile of shit

for sourcefile_attribute in sourcefile_attributes:
    value = sourcefile_attribute.get("value")
    if value in CHAR_BASE_AlphaTest_2S_dither_type:
        sourcefile_attribute.set("value", "CHAR_BASE_AlphaTest_2S_Dither")
# am I actually gonna finish this? tbh I should just do it manually since its so finicky.
