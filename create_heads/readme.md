requirement:
have python installed

what does this do?
automates the most annoying part of making custom heads:
* copying _merged.lsx reference head nodes (skeleton, visual, textures, material)
* generating UUID for these copies
* redirecting the skeleton, visual, and textures to your files.
* renaming the internal structure to your heads names.

e.g:
I have "Hazel_Head" which is based on "ELF_F_NKD_HEAD_A"
* copies the resources for ELF_F_NKD_HEAD_A's skeleton, visual, textures (HMVY, CLEA, NM), material.

* replaces the UUIDs for the copied resources. 
  * e.g: this is what happens to the skeleton UUID in both places it is mentioned.
    * `<attribute id="ID" type="FixedString" value="137b5984-0603-863d-4ffb-582c86c5861c" />`
    * becomes  `<attribute id="ID" type="FixedString" value="80630009-370a-4f2e-8a0f-5fad65f1e3db" />`
    * and
        `<attribute id="SkeletonResource" type="FixedString" value="137b5984-0603-863d-4ffb-582c86c5861c" />`
    * becomes
        `<attribute id="SkeletonResource" type="FixedString" value="80630009-370a-4f2e-8a0f-5fad65f1e3db" />`
* redirects to my files. 
  * e.g. this is what happens to the skeleton SourceFile and Template:
    * `<attribute id="SourceFile" type="LSString" value="Public/Shared/Assets/Characters/_Anims/Elves/_Female/ELF_F_NKD_Head_A_Base.GR2" />`
    * becomes `<attribute id="SourceFile" type="LSString" value="Generated/Hazel_Head/Hazel_Head_BASE.GR2" />`
    * and `<attribute id="Template" type="FixedString" value="Public/Shared/Assets/Characters/_Anims/Elves/_Female/ELF_F_NKD_Head_A_Base.Dummy_Root.0" />`
    * becomes `<attribute id="Template" type="FixedString" value="Generated/Hazel_Head/Hazel_Head_BASE.Dummy_Root.0" />`
      
* renames internal structure for consistency
  * e.g.:
    * `<attribute id="Name" type="LSString" value="ELF_F_NKD_Head_A" />`
    * becomes `<attribute id="Name" type="LSString" value="Hazel_Head" />` 
    * and `<attribute id="Name" type="LSString" value="ELF_F_NKD_Head_A_Base" />`
    * becomes `<attribute id="Name" type="LSString" value="Hazel_Head_Base" />`
    * and so forth

What does this not do?
* Does not generate "CharacterCreationAppearanceVisuals.lsx", you just need to copy the UUID in the textbox to the VisualResource.
    e.g.:
    ```<node id="CharacterCreationAppearanceVisual">
        <attribute id="BodyShape" type="uint8" value="0" />
        <attribute id="BodyType" type="uint8" value="1" />
        <attribute id="DefaultSkinColor" type="guid" value="3fbe1d26-86fd-8baf-d5e1-9ec3d0f499e9" />
        <attribute id="DisplayName" type="TranslatedString" handle="h05da87cegf86dg4cc3g9ce6g437b239d957b" version="4" /> <!-- HAZEL -->
        <attribute id="RaceUUID" type="guid" value="4f5d1434-5175-4fa9-b7dc-ab24fba37929" />
        <attribute id="SlotName" type="FixedString" value="Head" />
        <attribute id="UUID" type="guid" value="be7eb35c-5e4d-4e56-8a14-6435fc2705b0" />
        <attribute id="VisualResource" type="guid" value="b23b65d8-7ae8-42f2-81a3-b3d533b99b84" />
    </node>
  ```
    For this node replace the
    * `<attribute id="VisualResource" type="guid" value="b23b65d8-7ae8-42f2-81a3-b3d533b99b84" />`
      with the one generated in the text box.
    * `<attribute id="VisualResource" type="guid" value="%whatever_is_in_the_text_box%" />`

* Does not verify that your Reference Name exists inside your Reference File.
  * e.g: you must be sure that (ELF_F_NKD_HEAD_D) exists in your (_merged.lsx)

How do I use?

* in output_dir_path you must have these files:
    
    where %NAME% is the name of your folder/directory.
    
        %NAME%_BASE.GR2
        %NAME%.GR2
        %NAME%_HMVY.DDS
        %NAME%_NM.DDS
        %NAME%_CLEA.DDS
    e.g:
    
        output_dir_path = create_heads/Generated/Hazel_Head/
        skeleton = Hazel_Head_BASE.GR2
        head = Hazel_Head.GR2
        texture_clea = Hazel_Head_CLEA.DDS
        texture_hmvy = Hazel_Head_HMVY.DDS
        texture_nm = Hazel_Head_NM.DDS
    
* you must have a Reference XML with your reference head in it. 

    e.g.: I want to replace `ELF_F_NKD_HEAD_A` so I want the elf heads' `_merged.lsx`. Here is where I have that file on my pc:
  * 
      `reference_xml = 'C:\Users\emar\AppData\Local\Larian Studios\BG3_modding_tools\bg3-modders-multitool\UnpackedData\Shared\Public\Shared\Content\Assets\Characters\Elves\Heads\_merged.lsx'`
  * 
      you must have the name of the Reference Head you are using. e.g.: "ELF_F_NKD_HEAD_A"
  * 
      `reference_name = "ELF_F_NKD_HEAD_A"`

The Base XML should just be included in the `create_heads/source` folder as `base.xml`. Don't touch this as I have it set to create the region banks we need.
`base_xml = "create_heads/source/base.xml"`