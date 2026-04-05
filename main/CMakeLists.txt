idf_component_register(SRCS "attack_dos.c" "attack_method.c" "main.c" "attack_handshake.c" "attack_pmkid.c" "attack.c"
                    INCLUDE_DIRS .)
                    # REQUIRES esp_timer
                    # PRIV_REQUIRES wifi_controller frame_analyzer webserver pcap_serializer hccapx_serializer wsl_bypasser)
