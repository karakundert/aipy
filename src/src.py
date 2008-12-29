import fit

specials = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
    'Saturn', 'Uranus', 'Neptune']
src_data = {
    #             RA          DEC         FLUX  FREQ, INDEX ANGSIZE
    #'Moon'  : (None        , None,           0, .150,  0.10 ),
    #'Mercury': (None        , None,          0, .150,  0.10 ),
    #'Venus':   (None        , None,          0, .150,  0.10 ),
    #'Mars':    (None        , None,          0, .150,  0.10 ),
    #'Jupiter': (None        , None,          0, .150,  0.10 ),
    #'Saturn' : (None        , None,          0, .150,  0.10 ),
    #'Uranus' : (None        , None,          0, .150,  0.10 ),
    #'Neptune': (None        , None,          0, .150,  0.10 ),
    'Sun'  : (None, None, 57000, .150,  .55, 8.7e-3),
    'b0320': ('03:20:00.0', '-37:18:00',   259, .408, -0.8 , 0.),
    'pic'  : ('05:18:20.2', '-45:49:31',   452, .160, -0.8 , 0.),
    'hyd'  : ('09:18:00.3', '-12:05:39',  1860, .160, -2.30, 0.),
    'cen'  : ('13:22:34.3', '-42:44:15',  7104, .160, -0.52, 3.5e-3),
    #'her'  : ('16:45:27.2', '+05:18:25',  121, .160, -4.21, 0.),
    'her' : ('16:51:11.01', '5:04:58.4', 300.0, 0.159, -1, 0.000669),
    'sgr'  : ('17:45:40.0', '-29:00:28',  121, .160, -4.21, 0.),
    # Fluxes from Miriad:
    'crab' : ('05:34:28.3', '+22:01:30',  1838, .150, -0.30, 0.),
    'vir'  : ('12:30:44.4', '+12:22:54',   1446, .150, -0.86, 0.),
    'cyg'  : ('19:59:28.3', '+40:44:02', 10900, .150, -0.69, 0.),
    'cas'  : ('23:23:25.4', '+58:48:38',  9160, .150, -0.73, 0.),
    # 3C + 3CR Catalogs
    '3c2' : ('0:06:22.72', '-0:06:18.0', 16.5, 0.159, -0.84, 0.000727),
    '3c9' : ('0:20:25.27', '15:39:38.8', 15.5, 0.159, -0.29, 0.000436),
    '3c10' : ('0:25:25.06', '64:08:36.8', 110.0, 0.159, 1.75, 0.000960),
    '3c13' : ('0:34:16.53', '39:19:31.9', 12.0, 0.159, -1.18, 0.002909),
    '3c14' : ('0:36:12.13', '18:41:30.7', 13.5, 0.159, -3.11, 0.002909),
    '3c15' : ('0:37:51.47', '-1:14:30.5', 21.5, 0.159, -3.49, 0.005818),
    '3c16' : ('0:38:28.21', '13:06:29.1', 10.5, 0.159, 0.81, 0.000145),
    '3c17' : ('0:39:10.32', '-1:59:31.4', 21.5, 0.159, -0.21, 0.005818),
    '3c19' : ('0:40:55.19', '33:10:27.4', 13.0, 0.159, -3.26, 0.001745),
    '3c18' : ('0:40:05.72', '10:10:27.9', 16.5, 0.159, 2.94, 0.005818),
    '3c20' : ('0:44:23.64', '52:05:24.7', 30.0, 0.159, 2.77, 0.000145),
    '3c22' : ('0:51:00.43', '51:07:18.9', 13.5, 0.159, 0.63, 0.000291),
    '3c27' : ('0:55:55.25', '68:29:14.3', 22.0, 0.159, 0.77, 0.000291),
    '3c28' : ('0:55:50.49', '26:24:14.1', 19.5, 0.159, -2.94, 0.000436),
    '3c29' : ('0:57:36.31', '-1:18:47.9', 17.0, 0.159, -1.11, 0.000436),
    '3c31' : ('1:06:38.60', '32:27:01.9', 10.5, 0.159, 3.45, 0.000364),
    '3c33' : ('1:08:51.28', '13:20:59.1', 58.0, 0.159, -1.49, 0.000291),
    '3c34' : ('1:10:16.87', '31:39:57.3', 12.5, 0.159, -1.13, 0.000364),
    '3c35' : ('1:11:45.52', '47:20:55.5',  9.0, 0.159, 2.91, 0.000465),
    '3c36' : ('1:18:10.07', '45:38:46.7',  8.0, 0.159, 1.52, 0.000582),
    '3c40' : ('1:26:08.13', '-1:16:25.7', 26.0, 0.159, -0.71, 0.000727),
    '3c41' : ('1:26:43.49', '33:05:33.6',  8.5, 0.159, 1.44, 0.000436),
    '3c42' : ('1:27:40.30', '29:03:32.1', 12.0, 0.159, -0.38, 0.000364),
    '3c43' : ('1:29:58.64', '23:33:28.3', 16.5, 0.159, -3.20, 0.000436),
    '3c44' : ('1:30:27.21', '3:29:27.4',  8.0, 0.159, 2.82, 0.000291),
    '3c46' : ('1:36:29.62', '37:56:17.3', 12.5, 0.159, -2.43, 0.000364),
    '3c47' : ('1:36:25.97', '20:57:17.3', 27.0, 0.159, -2.66, 0.000233),
    '3c48' : ('1:37:42.45', '33:10:15.1', 50.0, 0.159, -0.55, 0.000145),
    '3c49' : ('1:41:12.72', '14:03:08.6', 10.0, 0.159, 1.24, 0.000582),
    '3c52' : ('1:50:25.05', '55:33:51.5',  9.5, 0.159, 0.45, 0.000436),
    '3c54' : ('1:55:28.97', '43:37:40.9', 11.5, 0.159, -1.24, 0.001745),
    '3c55' : ('1:57:10.42', '28:48:37.1',  7.5, 0.159, 9.12, 0.000364),
    '3c58' : ('2:05:27.47', '64:52:20.1', 13.0, 0.159, 5.43, 0.000654),
    '3c63' : ('2:20:56.35', '-1:56:18.2', 26.0, 0.159, -4.87, 0.005818),
    '3c66' : ('2:23:24.82', '43:04:36.4', 28.0, 0.159, 1.46, 0.000480),
    '3c65' : ('2:22:48.00', '39:59:37.9', 18.5, 0.159, 3.35, 0.000538),
    '3c67' : ('2:25:10.37', '30:07:31.6', 10.0, 0.159, -0.00, 0.000436),
    '3c69' : ('2:38:04.04', '59:11:58.4', 23.0, 0.159, -0.00, 0.001745),
    '3c71' : ('2:42:39.49', '-0:12:16.1', 11.0, 0.159, 1.81, 0.005818),
    '3c75' : ('2:57:05.75', '6:17:01.7', 38.0, 0.159, -4.45, 0.000524),
    '3c78' : ('3:08:34.34', '4:20:25.9', 17.0, 0.159, -1.11, 0.000291),
    '3c79' : ('3:10:01.71', '17:06:21.5', 34.0, 0.159, -3.09, 0.000218),
    '3c84' : ('3:19:47.50', '41:27:50.5', 50.0, 0.159, 1.31, 0.000335),
    '3c86' : ('3:27:24.84', '55:17:25.6', 19.0, 0.159, 0.89, 0.000364),
    '3c88' : ('3:27:50.74', '2:17:22.0',  9.0, 0.159, 5.10, 0.000465),
    '3c89' : ('3:34:18.65', '-1:04:00.5', 19.5, 0.159, -0.47, 0.000364),
    '3c91' : ('3:38:00.35', '51:00:48.5', 14.0, 0.159, -1.00, 0.002182),
    '3c93' : ('3:42:49.64', '5:11:29.5', 11.5, 0.159, -1.69, 0.000436),
    '3c98' : ('3:58:58.35', '10:32:30.2', 41.0, 0.159, -0.00, 0.000364),
    '3c99' : ('4:01:04.08', '0:25:21.9', 14.5, 0.159, -3.29, 0.000436),
    '3c103' : ('4:08:06.43', '43:00:56.8', 29.0, 0.159, -1.31, 0.005818),
    '3c105' : ('4:07:25.47', '3:42:57.8', 12.5, 0.159, 1.62, 0.000509),
    '3c107' : ('4:12:27.74', '-0:53:21.8', 11.5, 0.159, -0.39, 0.001745),
    '3c109' : ('4:13:40.64', '11:22:33.9', 19.5, 0.159, -0.00, 0.000218),
    '3c111' : ('4:18:25.54', '37:57:16.4', 60.0, 0.159, -0.45, 0.000422),
    '3c114' : ('4:21:10.13', '17:50:04.7', 12.5, 0.159, -1.98, 0.000436),
    '3c119' : ('4:32:36.40', '41:32:20.0', 14.5, 0.159, 0.30, 0.000218),
    '3c123' : ('4:37:04.18', '29:41:01.2', 204.0, 0.159, -1.36, 0.005818),
    '3c124' : ('4:40:51.24', '-2:13:15.5',  8.5, 0.159, 0.99, 0.000582),
    '3c125' : ('4:45:07.15', '37:32:28.6', 12.5, 0.159, -2.43, 0.000436),
    '3c129' : ('4:50:10.36', '45:04:08.2', 21.5, 0.159, -0.21, 0.000393),
    '3c130' : ('4:52:44.82', '51:50:58.1',  9.5, 0.159, 2.43, 0.000436),
    '3c131' : ('4:52:22.39', '29:14:58.1', 16.0, 0.159, -1.51, 0.000291),
    '3c132' : ('4:55:57.77', '22:54:42.7', 16.5, 0.159, -2.46, 0.000145),
    '3c133' : ('5:03:03.38', '25:24:13.0', 23.0, 0.159, -1.46, 0.006545),
    '3c134' : ('5:04:45.48', '38:07:06.5', 85.0, 0.159, -2.24, 0.005818),
    '3c135' : ('5:13:33.13', '1:15:27.3', 12.0, 0.159, 2.55, 0.000538),
    '3c137' : ('5:20:44.40', '50:50:59.3',  8.5, 0.159, 0.51, 0.005818),
    '3c138' : ('5:20:13.09', '13:59:59.2', 19.5, 0.159, -0.47, 0.000436),
    '3c141' : ('5:25:44.13', '32:44:36.4', 20.5, 0.159, -4.04, 0.005818),
    #'3c144' : ('5:34:31.53', '22:00:57.7', 1500.0, 0.159, -0.49, 0.000727),
    '3c147' : ('5:42:38.69', '49:52:24.3', 63.0, 0.159, -0.73, 0.000291),
    '3c152' : ('6:05:23.70', '20:29:42.9', 12.5, 0.159, -1.13, 0.001745),
    '3c153' : ('6:09:35.05', '48:03:26.4', 15.0, 0.159, 1.37, 0.005818),
    '3c154' : ('6:13:49.35', '26:03:06.4', 26.0, 0.159, -2.78, 0.000145),
    '3c157' : ('6:17:37.62', '22:41:49.6', 270.0, 0.159, -2.23, 0.004218),
    '3c158' : ('6:21:40.94', '14:29:31.5', 21.5, 0.159, -3.80, 0.001745),
    '3c165' : ('6:43:11.17', '23:22:58.8', 12.5, 0.159, -1.13, 0.000364),
    '3c166' : ('6:45:26.31', '21:16:49.0', 16.0, 0.159, -1.84, 0.000364),
    '3c171' : ('6:55:20.55', '54:04:08.9', 30.0, 0.159, -2.35, 0.006545),
    '3c173' : ('7:04:28.08', '40:09:29.1', 15.5, 0.159, -3.88, 0.000436),
    '3c172' : ('7:02:12.25', '25:17:37.8', 17.0, 0.159, -1.72, 0.000364),
    '3c175' : ('7:13:06.09', '11:49:51.5', 23.5, 0.159, -3.41, 0.006545),
    '3c177' : ('7:24:36.09', '15:29:04.2', 12.5, 0.159, -2.43, 0.000436),
    '3c180' : ('7:27:05.52', '-2:05:06.6', 15.0, 0.159, -0.61, 0.000436),
    '3c181' : ('7:28:10.01', '14:38:49.6', 14.0, 0.159, -0.66, 0.000364),
    '3c184' : ('7:37:44.31', '70:13:16.2', 17.0, 0.159, -3.86, 0.000364),
    '3c186' : ('7:44:24.81', '37:57:45.6', 14.0, 0.159, -0.32, 0.001745),
    '3c187' : ('7:45:01.65', '1:46:41.7',  9.0, 0.159, 1.78, 0.000436),
    '3c190' : ('8:01:40.55', '14:18:37.8', 12.0, 0.159, -0.77, 0.000582),
    '3c191' : ('8:04:54.35', '10:25:25.5', 11.0, 0.159, -0.41, 0.005818),
    '3c192' : ('8:05:37.45', '24:07:23.3', 17.0, 0.159, 1.22, 0.000364),
    '3c194' : ('8:09:46.61', '40:08:08.5', 12.5, 0.159, -2.91, 0.000436),
    '3c196' : ('8:13:39.63', '48:12:54.7', 66.0, 0.159, -0.99, 0.001745),
    '3c198' : ('8:22:36.52', '5:59:20.6', 16.0, 0.159, 0.27, 0.000538),
    '3c200' : ('8:28:14.90', '29:18:01.3', 10.5, 0.159, 1.89, 0.000436),
    '3c204' : ('8:37:26.70', '65:21:31.9',  9.0, 0.159, 0.48, 0.000436),
    '3c205' : ('8:39:23.59', '57:39:24.4', 11.0, 0.159, 1.13, 0.005818),
    '3c207' : ('8:43:15.30', '15:54:09.6', 10.0, 0.159, -0.00, 0.000436),
    '3c208' : ('8:53:11.94', '13:55:37.0', 24.5, 0.159, -3.77, 0.000364),
    '3c210' : ('8:58:04.08', '27:46:22.0', 10.0, 0.159, 0.43, 0.001745),
    '3c212' : ('8:58:45.92', '14:13:19.4', 21.5, 0.159, -2.90, 0.002182),
    '3c215' : ('9:05:41.38', '14:00:58.1', 15.5, 0.159, -3.88, 0.000436),
    '3c217' : ('9:10:01.21', '37:51:45.7', 10.5, 0.159, 1.18, 0.000364),
    '3c216' : ('9:09:39.24', '42:54:46.9', 23.5, 0.159, -2.12, 0.001745),
    '3c219' : ('9:21:11.93', '45:39:13.5', 42.0, 0.159, 0.41, 0.000145),
    '3c222' : ('9:36:37.89', '4:28:30.9', 12.0, 0.159, -2.55, 0.000582),
    '3c223' : ('9:37:56.98', '33:43:28.0', 14.0, 0.159, 0.31, 0.000364),
    '3c225' : ('9:42:19.19', '13:50:16.6', 19.5, 0.159, 2.20, 0.000436),
    '3c226' : ('9:44:21.33', '9:51:11.5', 11.0, 0.159, 1.81, 0.000364),
    '3c227' : ('9:47:49.56', '7:23:03.0', 50.0, 0.159, -5.14, 0.000407),
    '3c228' : ('9:50:08.01', '14:15:57.6', 17.0, 0.159, -0.54, 0.005818),
    '3c230' : ('9:52:00.74', '-0:06:07.0', 31.0, 0.159, -3.45, 0.001745),
    '3c231' : ('9:55:29.86', '69:50:46.8', 12.0, 0.159, 0.71, 0.000218),
    '3c234' : ('10:01:48.11', '28:46:31.2', 30.0, 0.159, -0.30, 0.005818),
    '3c236' : ('10:08:02.75', '37:00:18.0', 12.0, 0.159, -2.55, 0.000436),
    '3c237' : ('10:08:07.99', '7:32:17.5', 21.5, 0.159, 0.97, 0.001745),
    '3c238' : ('10:10:01.53', '3:11:13.6', 18.5, 0.159, -3.13, 0.000364),
    '3c239' : ('10:10:31.22', '44:18:13.0', 15.0, 0.159, -1.98, 0.000364),
    '3c241' : ('10:21:55.11', '21:55:50.6', 13.0, 0.159, -2.32, 0.006545),
    '3c245' : ('10:42:53.59', '12:06:15.9', 12.0, 0.159, -2.07, 0.005818),
    '3c247' : ('10:58:03.88', '43:06:55.8',  9.5, 0.159, 4.34, 0.000218),
    '3c249' : ('11:02:10.39', '-1:16:09.1', 14.5, 0.159, 2.85, 0.000364),
    '3c250' : ('11:08:52.83', '24:58:43.9', 14.0, 0.159, -2.14, 0.000436),
    '3c252' : ('11:10:46.26', '35:37:42.1', 15.0, 0.159, -1.98, 0.000291),
    '3c254' : ('11:14:40.41', '40:41:38.5', 21.5, 0.159, -1.10, 0.001745),
    '3c255' : ('11:19:07.33', '-6:39:25.4', 15.0, 0.159, 0.84, 0.000364),
    '3c256' : ('11:20:46.85', '23:24:33.4', 11.5, 0.159, -1.69, 0.001745),
    '3c257' : ('11:23:17.83', '5:35:31.5', 11.0, 0.159, -1.78, 0.000582),
    '3c258' : ('11:24:49.48', '19:22:30.4', 10.0, 0.159, -0.93, 0.000582),
    '3c263' : ('11:39:42.89', '65:50:22.2', 10.0, 0.159, 2.32, 0.002182),
    '3c264' : ('11:45:09.42', '19:43:20.2', 37.0, 0.159, -3.83, 0.000393),
    '3c265' : ('11:45:30.56', '31:29:20.1', 30.0, 0.159, -4.53, 0.000145),
    '3c266' : ('11:47:17.94', '51:46:19.6', 14.0, 0.159, -3.91, 0.000436),
    '3c267' : ('11:49:14.54', '12:53:19.1', 14.5, 0.159, -0.63, 0.000509),
    '3c270' : ('12:19:28.16', '5:58:20.9', 20.0, 0.159, 6.98, 0.000684),
    '3c272' : ('12:23:37.76', '42:20:22.5', 10.5, 0.159, -0.89, 0.000436),
    '3c273' : ('12:29:17.41', '2:05:25.2', 79.0, 0.159, -1.46, 0.001745),
    #'3c274' : ('12:30:49.82', '12:23:26.1', 1100.0, 0.159, -1.11, 0.000684),
    '3c275' : ('12:42:23.72', '-4:55:26.2', 18.0, 0.159, -5.66, 0.000436),
    '3c277' : ('12:52:53.45', '50:33:43.2', 12.0, 0.159, 0.36, 0.000582),
    '3c280' : ('12:56:59.16', '47:18:47.4', 25.0, 0.159, -1.98, 0.005818),
    '3c284' : ('13:11:56.09', '27:31:05.1', 10.0, 0.159, 0.43, 0.000436),
    '3c285' : ('13:22:23.32', '42:33:20.1', 11.0, 0.159, -0.41, 0.000436),
    '3c287' : ('13:31:25.62', '25:08:34.4', 29.0, 0.159, -6.45, 0.001745),
    '3c286' : ('13:31:07.65', '30:24:34.0', 30.0, 0.159, -3.16, 0.000218),
    '3c288' : ('13:38:49.39', '38:48:47.5', 15.0, 0.159, -0.30, 0.005818),
    '3c289' : ('13:46:55.57', '51:53:03.0', 12.0, 0.159, -2.07, 0.000364),
    '3c293' : ('13:52:15.72', '31:16:13.3', 12.5, 0.159, -0.36, 0.000364),
    '3c294' : ('14:06:44.86', '34:17:44.7', 12.5, 0.159, -2.91, 0.005818),
    '3c295' : ('14:11:19.11', '52:11:55.7', 74.0, 0.159, -0.12, 0.001745),
    '3c296' : ('14:16:14.34', '11:08:06.7', 10.0, 0.159, 1.98, 0.000436),
    '3c297' : ('14:18:06.41', '-4:11:48.9', 14.5, 0.159, -3.75, 0.000000),
    '3c298' : ('14:19:09.31', '6:32:13.8', 61.0, 0.159, -2.89, 0.000582),
    '3c299' : ('14:21:01.47', '41:40:19.1', 10.5, 0.159, 0.41, 0.000291),
    '3c300' : ('14:22:15.71', '17:11:21.7', 15.0, 0.159, 0.57, 0.000291),
    '3c303' : ('14:41:40.59', '51:51:14.6',  9.0, 0.159, 2.91, 0.005818),
    '3c305' : ('14:49:12.96', '63:20:37.2', 15.0, 0.159, -0.93, 0.001745),
    '3c310' : ('15:04:58.15', '26:02:23.4', 72.0, 0.159, -3.05, 0.000233),
    '3c313' : ('15:10:16.78', '7:57:39.8', 21.0, 0.159, 2.55, 0.000364),
    '3c315' : ('15:13:41.21', '26:07:51.3', 26.0, 0.159, -3.51, 0.000291),
    '3c317' : ('15:16:46.46', '7:00:01.0', 55.0, 0.159, -2.18, 0.005818),
    '3c318' : ('15:20:06.78', '20:17:12.4', 14.5, 0.159, -3.29, 0.002182),
    '3c319' : ('15:24:08.90', '54:28:27.5', 16.5, 0.159, 0.26, 0.000364),
    '3c320' : ('15:31:32.42', '35:42:51.9',  8.0, 0.159, 3.21, 0.005818),
    '3c321' : ('15:31:50.82', '24:07:52.5', 15.0, 0.159, -1.62, 0.005818),
    '3c322' : ('15:32:07.68', '53:48:54.9', 11.5, 0.159, -1.69, 0.000436),
    '3c323' : ('15:41:54.66', '60:08:30.3',  9.0, 0.159, 0.48, 0.000393),
    '3c324' : ('15:49:45.64', '21:23:56.6', 18.0, 0.159, -3.97, 0.005818),
    '3c325' : ('15:49:52.42', '62:40:59.7', 15.0, 0.159, -3.16, 0.005818),
    '3c326' : ('15:51:40.70', '17:38:03.5', 12.5, 0.159, -1.98, 0.000247),
    '3c327' : ('16:02:32.68', '1:56:43.7', 34.0, 0.159, 1.44, 0.000538),
    '3c330' : ('16:09:19.23', '66:02:13.9', 24.0, 0.159, -0.00, 0.000291),
    '3c332' : ('16:16:42.95', '30:01:39.6', 16.0, 0.159, -3.73, 0.000436),
    '3c334' : ('16:30:21.08', '17:37:33.4', 16.0, 0.159, -4.16, 0.005818),
    '3c336' : ('16:23:50.94', '23:41:07.5', 13.5, 0.159, -0.00, 0.005818),
    '3c341' : ('16:30:38.97', '30:02:35.1',  8.5, 0.159, 1.87, 0.000436),
    '3c338' : ('16:28:36.90', '39:31:27.4', 49.0, 0.159, -1.58, 0.000291),
    '3c337' : ('16:26:45.98', '44:13:20.3',  8.5, 0.159, 6.14, 0.000436),
    '3c340' : ('16:29:48.80', '23:33:31.4',  9.5, 0.159, 1.30, 0.000436),
    '3c343' : ('16:36:12.36', '62:45:00.6', 18.0, 0.159, -5.66, 0.000436),
    '3c345' : ('16:43:13.59', '40:05:27.0',  9.0, 0.159, 0.93, 0.001745),
    '3c346' : ('16:43:50.02', '17:18:28.4', 15.5, 0.159, -3.04, 0.002182),
    #'3c348' : ('16:51:11.01', '5:04:58.4', 300.0, 0.159, 0.71, 0.000465),
    '3c349' : ('16:59:34.37', '47:03:35.8', 13.5, 0.159, -1.04, 0.005818),
    '3c351' : ('17:04:40.83', '60:43:59.1', 15.0, 0.159, -2.75, 0.000436),
    '3c352' : ('17:10:41.17', '45:58:22.9', 12.0, 0.159, -0.77, 0.001745),
    '3c353' : ('17:20:32.75', '-0:54:57.2', 180.0, 0.159, 1.07, 0.000582),
    '3c356' : ('17:24:32.66', '51:10:23.0', 14.0, 0.159, 0.31, 0.000218),
    '3c357' : ('17:28:26.69', '31:47:38.4',  9.0, 0.159, -0.00, 0.000436),
    '3c368' : ('18:05:02.80', '10:57:16.9', 13.5, 0.159, 0.32, 0.000509),
    '3c371' : ('18:06:35.01', '69:55:29.8',  9.0, 0.159, 0.48, 0.000436),
    '3c380' : ('18:29:30.18', '48:45:05.8', 70.0, 0.159, -1.82, 0.002909),
    '3c381' : ('18:33:49.77', '47:26:24.5', 14.5, 0.159, -1.31, 0.002909),
    '3c382' : ('18:35:06.95', '30:25:28.8', 18.0, 0.159, 0.93, 0.000262),
    '3c386' : ('18:38:26.31', '17:13:42.5', 27.0, 0.159, -1.04, 0.000262),
    '3c388' : ('18:44:03.80', '45:35:08.4', 22.5, 0.159, -0.20, 0.005818),
    '3c390' : ('18:45:34.35', '9:52:12.9', 22.5, 0.159, -1.50, 0.005818),
    '3c389' : ('18:45:33.57', '-3:19:47.7', 17.0, 0.159, 1.87, 0.000480),
    '3c391' : ('18:49:21.81', '-0:55:31.3', 27.0, 0.159, -1.04, 0.000291),
    '3c392' : ('18:56:07.27', '1:18:57.6', 680.0, 0.159, -4.70, 0.002327),
    '3c394' : ('18:59:20.83', '13:00:11.8', 18.5, 0.159, -3.83, 0.000145),
    '3c396' : ('19:04:09.47', '5:35:31.8', 24.5, 0.159, -0.95, 0.000436),
    '3c397' : ('19:07:31.68', '7:11:46.0', 29.0, 0.159, -0.31, 0.000436),
    '3c398' : ('19:11:08.41', '9:14:01.2', 43.0, 0.159, 2.18, 0.000480),
    '3c400' : ('19:24:22.42', '13:48:56.0', 25.0, 0.159, 27.22, 0.008727),
    '3c401' : ('19:40:23.07', '60:42:03.6', 22.0, 0.159, -1.30, 0.005818),
    '3c402' : ('19:41:43.18', '50:39:07.7', 15.0, 0.159, -1.27, 0.000393),
    '3c403' : ('19:52:12.20', '2:30:46.4', 23.0, 0.159, 1.09, 0.000218),
    #'3c405' : ('19:59:27.86', '40:43:15.8', 8600.0, 0.159, -0.53, 0.000000),
    '3c409' : ('20:14:26.44', '23:35:10.9', 102.0, 0.159, -2.96, 0.004363),
    '3c410' : ('20:20:10.56', '29:40:31.8', 36.0, 0.159, -1.04, 0.001745),
    '3c411' : ('20:22:11.04', '10:08:38.4', 16.0, 0.159, -1.18, 0.004363),
    '3c418' : ('20:38:36.56', '51:17:37.1', 16.0, 0.159, -2.19, 0.000436),
    '3c424' : ('20:48:10.67', '7:01:07.2', 16.0, 0.159, -2.19, 0.005818),
    '3c428' : ('21:08:09.95', '47:32:10.9', 19.5, 0.159, -0.23, 0.000364),
    '3c430' : ('21:18:13.27', '60:47:41.0', 100.0, 0.159, -10.97, 0.000262),
    '3c431' : ('21:18:53.98', '49:34:42.2', 31.0, 0.159, -3.45, 0.000218),
    '3c432' : ('21:22:50.57', '17:16:52.5', 13.5, 0.159, -1.42, 0.005818),
    '3c433' : ('21:23:45.06', '25:00:55.1', 62.0, 0.159, -1.56, 0.004363),
    '3c434' : ('21:24:53.71', '16:01:58.1', 10.5, 0.159, -0.00, 0.000509),
    '3c435' : ('21:29:07.26', '7:40:09.5', 12.5, 0.159, -2.43, 0.005818),
    '3c436' : ('21:44:09.78', '28:03:48.6', 21.0, 0.159, -2.98, 0.005818),
    '3c437' : ('21:47:23.74', '15:16:56.2', 16.0, 0.159, -3.73, 0.005818),
    '3c438' : ('21:55:54.79', '37:56:16.5', 43.0, 0.159, -1.33, 0.005818),
    '3c441' : ('22:06:57.78', '29:27:40.5', 12.5, 0.159, 0.35, 0.005818),
    '3c442' : ('22:12:57.84', '11:04:52.5', 33.0, 0.159, -4.44, 0.000000),
    '3c445' : ('22:23:05.78', '-2:02:48.3', 20.5, 0.159, 1.02, 0.000276),
    '3c449' : ('22:31:22.02', '39:12:26.4', 11.5, 0.159, 1.42, 0.000436),
    '3c452' : ('22:45:45.95', '39:36:48.6', 50.0, 0.159, -0.18, 0.000465),
    '3c454' : ('22:49:53.87', '16:05:54.1', 11.5, 0.159, -2.17, 0.000436),
    '3c455' : ('22:55:56.27', '13:28:01.8', 15.0, 0.159, -1.27, 0.000364),
    '3c456' : ('23:11:50.40', '9:22:19.0', 10.0, 0.159, 2.32, 0.000436),
    '3c458' : ('23:12:09.41', '5:25:19.3', 12.5, 0.159, -1.98, 0.000320),
    '3c459' : ('23:16:37.81', '4:11:23.3', 25.0, 0.159, -1.13, 0.000436),
    '3c460' : ('23:20:43.55', '23:53:26.6', 13.0, 0.159, -2.78, 0.000364),
    #'3c461' : ('23:23:27.76', '58:48:28.8', 13000.0, 0.159, -1.48, 0.000000),
    '3c465' : ('23:38:27.38', '26:54:37.3', 50.0, 0.159, -3.16, 0.000582),
    '3c470' : ('23:56:25.36', '44:04:42.0',  8.0, 0.159, 1.04, 0.000364),
}

def get_src(s):
    """Return a source created out of the parameters in the dictionary srcs."""
    if not type(s) == str: return s
    ra, dec, st, mfreq, index, angsize = src_data[s]
    if s in specials:
        return fit.RadioSpecial(s, st, mfreq=mfreq, 
            index=index, angsize=angsize)
    else:
        return fit.RadioFixedBody(ra, dec, janskies=st, mfreq=mfreq, 
            index=index, name=s, angsize=angsize)

def get_catalog(srcs=None, cutoff=None):
    if srcs is None:
        if cutoff is None: srcs = src_data.keys()
        else: srcs = [s for s in src_data if src_data[s][2] > cutoff]
    srcs = [get_src(s) for s in srcs]
    return fit.SrcCatalog(srcs)
