class ConstantIdError(KeyError):
    """Constant key does not exist."""
    pass


class ConstantNameError(KeyError):
    """Constant name does not exist."""
    pass


class Constant:
    """Expose Dundas constants with human names"""

    # There is not way to get the constants from the rest API.
    # To find them I got the list from the documentation page:
    # https://www.dundas.com/support/api-docs/js/#API%20Reference/dundas/constants.html
    # And then got the IDs in javascript:
    # cs = [ADMIN_ACCOUNT_ID", "ALL_TOKEN_DEFINITION_ID", ...];
    # for (i=0; i<cs.length; i++) {
    #     console.log("        \"" + cs[i] + "\": \"" + dundas.constants[cs[i]]+ "\",")
    # }
    # I am not convinced it is foolproof, but it looks quite good.
    constants = {
        "ADMIN_ACCOUNT_ID": "92ace8aa-757c-44d1-a701-6234ed210fbb",
        "ALL_TOKEN_DEFINITION_ID": "e6c4688e-bb68-4060-9a50-334bb114fbd4",
        "APPEND_DATE_TO_FILE_NAME_ID": "4ab81086-0857-427f-9d22-bafb9abe9ef4",
        "AUTO_SAVE_TIMER": "10000",
        "CELL_PROPERTY_CONTEXTUAL_VALUE_ID_KEY": "ValueId",
        "CHART_SIMPLIFICATION_RULE_ID": "a9d1e5e8-ec64-47b7-8e05-2d79f8ec232b",
        "CHART_STACK_VALUE_ID": "255b06c0-1670-1ecd-4e67-f5e4e06e2be3",
        "CONFIG_SETTING_ACCOUNT_REGISTRATION_ENABLED": "7a48530b-4367-4041-8aa7-662e2feb26a1",
        "CONFIG_SETTING_ALLOW_USER_NAME_IN_PASSWORD": "18e09e31-7754-400e-b8cf-c39227d5ade9",
        "CONFIG_SETTING_ANONYMOUS_USER_NAME": "555C7EF0-9A41-4903-9D59-22EE7026C560",
        "CONFIG_SETTING_CLEANUP_INTERVAL": "7968e638-6188-4fb9-97c7-a2b3beb26b67",
        "CONFIG_SETTING_CROSS_ORIGIN_RESOURCE_SHARING_ORIGINS": "2a681a83-e807-4be6-8c79-6c351b0e2ca6",
        "CONFIG_SETTING_DEFAULT_THEME": "0752cd39-078f-4796-a2b7-51cdcf45c67f",
        "CONFIG_SETTING_IS_AUTO_SAVE_DISABLED": "8fa2278e-fbef-4569-b150-0a5da3e17352",
        "CONFIG_SETTING_IS_ERROR_SENDING_DISABLED": "d1ec3486-52f2-4fea-ba7b-3ac69956daf5",
        "CONFIG_SETTING_IS_ERRORS_IGNORED": "0481501f-a0cf-4daa-94f2-9abf087727be",
        "CONFIG_SETTING_IS_SPLASH_SCREEN_DISABLED": "fdc0d281-352c-4a81-969d-6fe83dd1f18f",
        "CONFIG_SETTING_LOG_ON_MODES": "0675bd86-2cc6-45bf-a4e3-f47684fc902a",
        "CONFIG_SETTING_NOTIFICATION_ALLOW_USER_SPECIFIED_EMAIL_RECIPIENTS": "f317af59-1b95-4493-aaef-364f520d0195",
        "CONFIG_SETTING_NOTIFICATION_ALLOWED_USER_SPECIFIED_EMAIL_RECIPIENT_DOMAINS":
            "7ff5e73a-4cc0-4849-816a-b135e014c73a",
        "CONFIG_SETTING_PASSWORD_MINIMUM_LENGTH": "22b8fb8b-2b2d-4f29-b95f-89e17d666ab7",
        "CONFIG_SETTING_PASSWORD_POLICY_ALLOW_CHANGE": "0f0a0e3d-b49e-4b7b-a048-5f859953d913",
        "CONFIG_SETTING_REQUIRE_MIXED_ALPHANUMERIC_PASSWORD": "3f214ddd-edac-4f5b-85e0-9be530a3c1aa",
        "CONFIG_SETTING_REQUIRE_MIXED_CASE_PASSWORD": "448a2233-c1ff-4950-b733-b8237207b230",
        "CONFIG_SETTING_REQUIRE_SYMBOL_IN_PASSWORD": "5eb3978d-1567-4a43-8116-0b635c5dcc39",
        "CONFIG_SETTING_UI_FILE_CACHE_MAX_COUNT": "5c818aab-b046-4025-bc13-de241f9f8643",
        "CSV_ADAPTER_ID": "19729b41-499e-4a18-9d05-c639be62a2bd",
        "CURRENT_DEFAULT_VIEW_USER_DATA_KEY": "dundas_webapp_default_view",
        "CURRENT_HOME_LAYOUT_USER_DATA_KEY": "227c3c21-a15f-44e1-ab01-2a3b1480f25f_dundas_webapp_home_layout",
        "CURRENT_PROJECT_ID_USER_DATA_KEY": "dundas_webapp_projectid",
        "DATA_CUBE_CREATION_TYPE_KEY": "creationType",
        "DATA_INPUT_CREATED_BY_NAME": "CreatedBy",
        "DATA_INPUT_CREATED_TIME_NAME": "CreatedTime",
        "DATA_INPUT_LAST_MODIFIED_BY_NAME": "LastModifiedBy",
        "DATA_INPUT_LAST_MODIFIED_TIME_NAME": "LastModifiedTime",
        "DATA_INPUT_RECORD_ID_NAME": "RecordId",
        "DATA_INPUT_RECORD_SEQUENCE": "RecordSequence",
        "DATA_PREFIX_QUERY_STRING_KEY": "dundas_webapp_data_querystring_key",
        "DATA_PROPERTY_ENABLED_SLICER_AS_SUBQUERY": "ENABLE_SLICER_AS_SUBQUERY",
        "DATA_PROPERTY_IS_IN_PRIMARY_KEY": "IsInPrimaryKey",
        "DATA_PROPERTY_IS_UTILITY_HIERARCHY": "IS_UTILITY_HIERARCHY",
        "DATA_PROPERTY_SECURITY_ATTRIBUTE_ID": "SecurityAttributeId",
        "DATA_PROPRETY_IS_RAGGED_LEAF": "IsRaggedLeaf",
        "DATARETRIEVAL_BULK_CALL_DELAY_MS": "10",
        "DEFAULT_TOKEN_DEFINITION_ID": "9cb0dba7-4c9e-49cd-9383-e9bc1c5397f1",
        "DEFAULT_VIEW_CUSTOM_ATTRIBUTE_ID": "9822692a-bd03-4cd2-8784-da14c6fe1636",
        "DELETE_REASON_FOLDER_NOT_EMPTY": "FolderNotEmpty",
        "DELETE_REASON_REFERENCED": "Referenced",
        "DESIGNER_MODE_QUERY_STRING_KEY": "m",
        "DEVELOPERS_GROUP": "a63d43b6-efc2-40c0-bb18-4d443ca8560e",
        "EDIT_QUERY_STRING_KEY": "e",
        "EMPTY_GUID": "00000000-0000-0000-0000-000000000000",
        "END_OF_CURRENT_YEAR_TOKEN_DEFINITION_ID": "1069693e-1d5f-43f0-85e8-70f00060c82e",
        "EVERYONE_GROUP": "EEEB023D-18F4-423E-99B9-8D25667671E2",
        "EXCEL_ADAPTERS_ID": "27674367-5117-4b44-8972-0ab668b9a20e",
        "EXCEL_EXPORT_SELECTION_ID": "482e5d18-4183-493a-9cdc-f3adf9637f79",
        "EXCEL_INCLUDE_PARAMETERS_ID": "de83b54d-1e2c-44b5-9466-1f25eb1274f6",
        "EXCEPTION_DETAILS_MESSAGE_KEY": "9135a7f0-476d-48ac-b5ab-eb7cea7499b2",
        "EXCEPTION_DISPLAY_DEFAULT_KEY": "4367b70f-a059-4aa2-aa9f-c8b2c0e9fa56",
        "EXCEPTION_ERROR_CODE_KEY": "909b8f52-b861-4ac0-8bcf-69d69f06c213",
        "EXCEPTION_HELP_TOPIC_REFERENCE_KEY": "e677d679-e449-45a7-b4d2-d62b7819e69f",
        "EXCEPTION_SUPPLEMENTAL_MESSAGE_KEY": "0c493813-698c-465a-8da5-b62bcb531b19",
        "EXCEPTION_VERSION_NUMBER_KEY": "4052bf36-e432-4131-9d42-cc2c96bdf040",
        "EXPORT_IS_DOWNLOAD_LINK_QUERY_STRING_KEY": "isDownloadLink",
        "FILE_METADATA_CUBE_HYPERGRAPH_TIMESTAMP": "HypergraphTimestamp",
        "FILE_METADATA_CUBE_STORAGE_TYPE_KEY": "CubeStorageType",
        "FILE_METADATA_CUBE_WAREHOUSE_TIMESTAMP": "WarehouseTimestamp",
        "FILE_METADATA_DATA_CONNECTOR_DATA_RESOURCE": "DataSourceResourceId",
        "FILE_METADATA_DATA_CONNECTOR_IGNORE_DISCOVERY": "IgnoreDiscovery",
        "FILE_METADATA_PIXEL_HEIGHT": "pixelHeight",
        "FILE_METADATA_PIXEL_WIDTH": "pixelWidth",
        "FILE_METADATA_RECYCLED_INFO": "recycledInfo",
        "FILE_METADATA_VIEW_THUMBNAIL": "ThumbnailGenerationDate",
        "GLOBAL_PROJECT_ID": "a3a952c9-5092-444b-bc9a-28e1d013ffa4",
        "HELP_LINK_TOPIC_REFERENCE_QUERY_STRING_KEY": "topicReference",
        "HIERARCHY_CREATION_TYPE_KEY": "creationType",
        "HIERARCHY_RAGGED_TYPE": "r",
        "HIERARCHY_STANDARD_TYPE": "s",
        "HIERARCHY_UKNOWN_TYPE": "u",
        "IMAGE_RESOURCE_PROTOCOL": "dundasImageResource:",
        "INCLUDE_ADAPTER_IMAGES_ID": "d614e156-7908-499b-ba79-23cac5e84aea",
        "INVALID_SESSION_HTTP_STATUS_CODE": "440",
        "IS_EXPORT_QUERY_STRING_KEY": "isExport",
        "LEGACY_EXPORT_ID": "885dcdcb-7975-4f86-870d-77eb50d81b72",
        "LICENSE_CONFLICT_DETECTED_KEY": "36ff4659-0aee-4db5-9ca1-b41aae62652a-RECOVERY",
        "LOADING_OVERLAY_DELAY": "500",
        "MAX_CHECK_IN_COMMENT_LENGTH": "1900",
        "MAX_ENTITY_NAME_LENGTH": "300",
        "MEASURE_NAME_USAGE_UNIQUE_NAME": "edfd2a84-97a7-4812-ac10-227a7eabb50b",
        "METRIC_SET_BULK_CALL_DELAY_MS": "50",
        "METRIC_SET_GENERATE_ID": "mid",
        "METRIC_SET_PREVIOUS_ADAPTER_ID": "aid",
        "METRIC_SET_PREVIOUS_VIEW_ID": "pvid",
        "MULTI_TENANCY_ID": "f36f9244-f363-4f6b-bf54-779d1c0e8123",
        "NO_SELECTION_TOKEN_DEFINITION_ID": "f3c43ff6-2f59-41c5-b6e9-101743475a1b",
        "NOTIFICATION_ID_QUERY_STRING_KEY": "notificationId",
        "NOW_TOKEN_DEFINITION_ID": "44a432cd-0076-47b2-b032-662c4a7f77ea",
        "NULL_TOKEN_DEFINITION_ID": "2f5774bf-20e3-44cb-aac9-8a20666c9a16",
        "OLAP_CUBE_QUERY_STRING_KEY": "vc",
        "OLAP_NATIVE_CUBE_ID_QUERY_STRING_KEY": "nativeCubeId",
        "OPEN_RANGE_BOUNDARY_TOKEN_DEFINITION_ID": "e3f7a7e8-5b91-4a6c-943d-6e7134e54ca0",
        "PARENT_ID_QUERY_STRING_KEY": "parentId",
        "PATH_SEPARATOR": "/",
        "PDF_BOTTOM_MARGIN_ID": "79803dfd-c4ba-4bff-8f52-06011e8722ee",
        "PDF_LEFT_MARGIN_ID": "a9dc7738-e8fd-440d-8466-007bbcc3f672",
        "PDF_ORIENTATION_ID": "2d51f548-f554-4e4a-9948-fbb3e4694fbe",
        "PDF_PAPER_HEIGHT_ID": "e1458586-5c7f-41e2-bc51-f0fe744f2715",
        "PDF_PAPER_MEASUREMENT_UNIT_ID": "dc3732ee-d69e-4df4-9452-a733825ee7f2",
        "PDF_PAPER_SIZE_ID": "bbe12d5c-9713-4b2c-9bf9-61b40f9b1794",
        "PDF_PAPER_WIDTH_ID": "c781832c-64c2-4e4d-86d4-ae149b52add6",
        "PDF_RIGHT_MARGIN_ID": "d72635db-eb31-435c-ad83-b1dedf59f692",
        "PDF_TOP_MARGIN_ID": "497eaf10-42f2-4eec-b2bf-2584eef6e323",
        "PHONE_INNER_WIDTH_SIZE": "768",
        "PNG_ADAPTER_ID": "d1abb1e7-6efe-45cd-b11f-a89dd8532ddd",
        "PNG_EXPORT_SELECTION_ID": "63a56f59-6a01-4733-82aa-6f5531b88b8d",
        "PNG_THUMBNAIL_WIDTH_HEIGHT_ID": "a6f08189-01f7-44e4-939c-ed9707ef57ed",
        "POPUP_CONTAINER_ID": "popup-window-content",
        "POWER_USERS_GROUP": "fb98acac-4343-4290-aa87-d4c4e75e20ee",
        "PREDEFINED_TEMPLATES_TAG": "Predefined Templates",
        "PRIVILEGE_ALLOW_DEFAULT_VIEW_OVERRIDE": "74cd9f29-f357-41ee-b024-bf70645e737e",
        "PRIVILEGE_CHANGE_DATA_ID": "5643fb10-49f3-430c-b973-dfbeb7cc8d6c",
        "PRIVILEGE_CONTEXT_MENU_ID": "dd085006-9606-4917-9481-00fa24e0bc62",
        "PRIVILEGE_CREATE_TOKENS": "1201bd5f-e2c0-4dbd-bbfe-4ddaed55668c",
        "PRIVILEGE_DATA_BINDING_PANEL_ID": "f7af8b10-bb01-4406-94c3-0dcafa65b529",
        "PRIVILEGE_DATA_CUBE_IN_MEMORY_STORAGE": "54d4c811-b4a7-4e5c-a90f-cacd5983800c",
        "PRIVILEGE_DATA_CUBE_WAREHOUSE_STORAGE": "4fcc3ce1-05c5-432b-9603-78baa1d30374",
        "PRIVILEGE_DATA_INPUT": "02b028a4-d8a2-467b-8df9-489ce9d091bc",
        "PRIVILEGE_DATA_PREVIEW": "ca11607c-babb-4c0d-bfbd-65bd9cac9162",
        "PRIVILEGE_EDIT_ID": "9918f49d-8388-4e4a-91c9-21c54a81edf0",
        "PRIVILEGE_EDIT_MY_OWN_COPY_ID": "78cd3a03-7f34-4f98-be7b-319638135838",
        "PRIVILEGE_FULL_SCREEN_ID": "f630715c-e6ef-4256-aec5-2ef92ee12f5d",
        "PRIVILEGE_MEASURE_CORRECTIONS": "8ea8bfbc-a6b9-42ff-9cee-0b020d000d7c",
        "PRIVILEGE_MEASURE_INPUT": "0f1bcaf9-3fa3-4ff9-b26e-1cb420ffe504",
        "PRIVILEGE_MODIFY_DATA_ID": "93056b15-05f4-4216-8946-fe29eaef33c6",
        "PRIVILEGE_NOTE_ID": "a2456f94-173f-40af-8693-9965d0d884b9",
        "PRIVILEGE_NOTIFICATION_ID": "4003864a-853a-423a-b02f-557ec2388a9c",
        "PRIVILEGE_RE_VISUALIZE_ID": "a3bf892e-48db-4794-96ac-3c54f5e77aa9",
        "PRIVILEGE_SETUP_INTERACTIONS_ID": "e7aa82f6-db5d-491c-8af2-b7a176cb4eb5",
        "PRIVILEGE_SHARE_ID": "dfc14516-ecaa-47d3-902d-2bd861c13bff",
        "PRIVILEGE_SIMPLE_PROPERTY_PANEL_ID": "71848979-66aa-4bea-8abc-b4f196c1c983",
        "PRIVILEGE_SORTING_FILTERING_ID": "224516ab-3aab-4b5f-a856-b6f9efd8ae1e",
        "PRIVILEGE_STORE_USER_UI_CUSTOMIZATIONS": "adb4491a-c547-4f5b-88b1-a1098491cf0f",
        "PRIVILEGE_STORE_VIEW_PERSONALIZATION": "59f37487-741c-4970-8eae-855ce5799825",
        "PRIVILEGE_TOOLBAR_ID": "d340b53e-bfee-4e25-81d8-645519439925",
        "PRIVILEGE_UNSAFE_TRANSFORM_ACCESS": "b308317a-35f2-4c6b-a19a-9dbf59a7ef2a",
        "PROJECT_ID_QUERY_STRING_KEY": "projectId",
        "PROJECTS_ROOT_FOLDER_ID": "b1668d22-840e-4fa1-80df-958d58bff12d",
        "RAGGED_ALL_MEMBERS_TOKEN_ID": "6b48acc0-54a7-4d8d-aea9-0e1c912918ad",
        "RAGGED_LEAF_MEMBERS_TOKEN_ID": "fd0e6434-7ca7-4ad3-b64d-fcd8c3cdfb83",
        "REBUILD_INDEXS_JOB_ID": "4323f2f1-a8b8-459b-9ef4-52f3a7914300",
        "RECYCLE_BIN_ROOT_FOLDER_ID": "0379ac09-8e16-4f27-b4e6-a7e459180864",
        "REDO_COMMAND_STATE_KEY": "redoCommand",
        "RESOURCE_ID_QUERY_STRING_KEY": "resourceId",
        "SERVER_ONLY_USER_DATA_KEY_PREFIX": "227c3c21-a15f-44e1-ab01-2a3b1480f25f",
        "SESSION_ID_QUERY_STRING_KEY": "sessionId",
        "SESSION_PING_TIMER": "60000",
        "SHORT_LINK_QUERY_STRING_KEY": "shortLink",
        "STANDARD_CREATEFILE_DELIVERY_PROVIDER_ID": "3b192991-f37f-4311-940b-f234e62ba471",
        "STANDARD_CSV_EXPORT_PROVIDER_ID": "07d7e096-ff2b-4da2-84a5-58b27fb67cdc",
        "STANDARD_DATA_INPUT_TRANSFORM_ID": "a7de0d91-177b-407e-976d-5092ba68ed47",
        "STANDARD_EMAIL_DELIVERY_PROVIDER_ID": "9effc739-a6be-4272-a63f-375e1645d6a7",
        "STANDARD_EXCEL_EXPORT_PROVIDER_ID": "679e6337-48aa-4aa3-ad3d-db30ce943dc9",
        "STANDARD_EXPORT_NAME_PREFIX_ID": "ob95611baftw5fybc33pkoohkh",
        "STANDARD_IMAGE_EXPORT_PROVIDER_ID": "9a15b21e-fa9e-4ece-8b31-9e12f1c6134a",
        "STANDARD_PDF_EXPORT_PROVIDER_ID": "5752eb39-40b5-4d79-b96b-9f9297c67193",
        "STANDARD_POWERPOINT_EXPORT_PROVIDER_ID": "b58d4c94-9f4f-4d38-800b-2b5d4d348625",
        "STANDARD_PYTHON_GENERATOR_TRANSFORM_ID": "76588681-98D0-453A-9C25-7A56AD42C222",
        "STANDARD_R_GENERATOR_TRANSFORM_ID": "842A090C-0CB6-41ED-8F6C-0E4D6A9EDB64",
        "STANDARD_RESULT_TRANSFORM_ID": "b54baf74-43e7-4941-b18a-3ab5b2591480",
        "STANDARD_USERS_GROUP": "00d544b9-bfad-434a-acd9-f2bd7a93f6f8",
        "SYSTEM_ADMINISTRATORS_GROUP": "23422323-0CD3-42B7-BAA6-8A73E00BA6C1",
        "SYSTEM_CLEANUP_JOB_ID": "3c8bce75-45cd-4839-a406-a0068eb47f20",
        "SYSTEM_SERVICE_ID": "90ac7b78-62e7-41d9-b16b-c298aadfade5",
        "TEMP_FOLDER_ID": "76fb5175-b732-4251-a96e-b8368887fa4e",
        "TEMPLATE_LEFT_SPLIT_ID": "d4d8d79d-d274-4f73-ad76-a0271e378d39",
        "TEMPLATE_QUADRANT_ID": "524ce722-c6c8-4dbf-a872-5f5f59738a40",
        "TEMPLATE_QUERY_STRING_KEY": "template",
        "TEMPLATE_RIGHT_SPLIT_ID": "aa25fc89-9606-4b5f-bfe3-d416b7c704cc",
        "TEMPLATE_THREE_COLUMN_ID": "3b331d52-c753-4485-adb6-45f5d4b2d520",
        "TEMPLATE_THREE_ROW_ID": "df7b59ff-5644-49c3-906c-b0b2174e4b2b",
        "TEMPLATE_TWO_COLUMN_ID": "4b8644e0-0a09-4bd6-969e-4c552b01362d",
        "TENANT_PROJECTS_ROOT_FOLDER_ID": "710c07a1-7edd-4609-ad2f-8e1426ea0a46",
        "TOKEN_PARAMETER_RESOLVE_CALL_DELAY_MS": "10",
        "TRANSFER_FILE_EXTENSION": "dbie",
        "TREEMAP_SIMPLIFICATION_RULE_ID": "6affc832-e616-b42f-fee3-c835d6d65361",
        "TUPLE_PROPERTY_RECORD_ID_KEY": "RecordId",
        "UNDO_COMMAND_STATE_KEY": "undoCommand",
        "USER_PROJECTS_ROOT_FOLDER_ID": "587ebce0-be40-415b-aefc-ab520fc38ba6",
        "USER_SETTINGS_ADMIN_SECTION": "adminSectionSettings",
        "USER_SETTINGS_ADMIN_SECTION_APPCONFIG": "adminSectionSettings_AppConfig",
        "USER_SETTINGS_ADMIN_SECTION_HOME": "adminSectionSettings_Home",
        "USER_SETTINGS_CUBEPERSPECTIVE_DESIGNER": "cubeperspectiveDesignerSettings",
        "USER_SETTINGS_DASHBOARD_DESIGNER": "dashboardDesignerSettings",
        "USER_SETTINGS_DATACUBE_DESIGNER": "datacubeDesignerSettings",
        "USER_SETTINGS_HIERARCHY_DESIGNER": "hierarchyDesignerSettings",
        "USER_SETTINGS_HOME_SCREEN": "homeScreenSettings",
        "USER_SETTINGS_METRICSET_DESIGNER": "metricsetDesignerSettings",
        "USER_SETTINGS_REPORT_DESIGNER": "reportDesignerSettings",
        "USER_SETTINGS_SCORECARD_DESIGNER": "scorecardDesignerSettings",
        "USER_SETTINGS_SLIDESHOW_DESIGNER": "slideshowDesignerSettings",
        "VIEW_BULK_CALL_DELAY_MS": "50",
        "VIEW_ID_QUERY_STRING_KEY": "viewId",
        "VIEW_OPTIONS_QUERY_STRING_KEY": "vo",
        "VIEW_OPTIONS_STATE_KEY": "viewOptions",
        "VIEW_OVERRIDES_QUERY_STRING_KEY": "overrides",
        "VIEW_OVERRIDES_STATE_KEY": "overrides",
        "VIEW_PARAMETER_QUERY_STRING_VALUE_PREFIX": "$",
        "VIEW_PERSONALIZATION_SHORT_LINK_CATEGORY_ID": "25f614d2-eaa1-4888-bf25-fb0461cc8aa9",
        "WEB_API_PATH": "api/",
        "WEB_APP_MODULE_ID": "21259d43-ee4c-4b06-b73f-c9c2cdce60c6",
    }

    def __init__(self, *irrelevantargs, **irrelevantkwargs):
        # Move constants one level up for easy access.
        for name, uuid in self.constants.items():
            setattr(self, name, uuid)

    @classmethod
    def getNamesById(cls, id):
        """Get names, potentially more than one, for one ID."""
        names = []
        for k, v in cls.constants.items():
            if v.lower() == id.lower():
                names.append(k)
        if names:
            return names
        else:
            raise ConstantIdError("Could not find constant with id '{}'.".format(id))

    @classmethod
    def getIdByName(cls, name):
        try:
            return cls.constants[name.upper()]
        except KeyError as e:
            # from None hides the original KeyError, which is redundant.
            raise ConstantNameError("Could not find constant with name '{}'".format(name)) from None
