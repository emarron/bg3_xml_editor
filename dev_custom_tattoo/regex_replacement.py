import re

s = "ELF_F_NKD_Head_A.ELF_F_NKD_Head_A_Mesh.0"
s2 = '<attribute id="MapKey" type="FixedString" value="ELF_F_NKD_Head_A.ELF_F_NKD_Head_A_Mesh.0" />'
pattern = r"(\w)_NKD_Head_(.*?)(\..*)_NKD_Head_(.*?)_Mesh\."
replacement = r"\1S_NKD_HEAD_\2_Remap\3S_NKD_HEAD_\4_Remap_Mesh."

new_s = re.sub(pattern, replacement, s)

print(new_s)  # Output: ELF_FS_NKD_Head_A_Remap.ELF_FS_NKD_Head_A_Remap_Mesh.0
new_s = re.sub(pattern, replacement, s2)
print(new_s)