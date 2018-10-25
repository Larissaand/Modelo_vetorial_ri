import numpy as np

class ModelScore(object):
        def __init__(self):
                self.rs = list([])
                self.dict = { "Is CF mucus abnormal?": [3, 47, 50, 60, 114, 132, 135, 139, 151, 169, 189, 190, 197, 200, 226, 256, 265, 297, 298, 299, 311, 312, 325, 333, 343, 347, 349, 369, 370, 371, 374, 386, 392, 410, 420, 427, 428, 430, 434, 437, 439, 440, 441, 450, 461, 465, 478, 496, 497, 498, 499, 500, 501, 502, 503, 505, 511, 513, 516, 520, 524, 531, 533, 549, 553, 559, 561, 568, 590, 592, 593, 604, 605, 633, 669, 701, 702, 710, 711, 722, 724, 729, 731, 733, 750, 761, 763, 772, 779, 788, 805, 843, 845, 856, 857, 861, 864, 867, 875, 876, 888, 889, 895, 925, 935, 943, 944, 975, 980, 982, 990, 1000, 1019, 1038, 1040, 1064, 1076, 1080, 1088, 1091, 1092, 1093, 1098, 1144, 1156, 1175, 1185, 1188, 1196, 1223, 1226],\
"What are the hepatic complications or manifestations of CF?": [17, 59, 63, 72, 91, 95, 97, 98, 99, 135, 149, 174, 197, 204, 205, 226, 232, 238, 266, 297, 301, 322, 339, 350, 354, 355, 364, 370, 385, 398, 408, 410, 413, 414, 420, 422, 423, 424, 426, 434, 443, 474, 545, 549, 550, 601, 603, 611, 642, 643, 657, 673, 690, 700, 720, 722, 724, 725, 729, 731, 735, 747, 752, 763, 764, 767, 792, 794, 816, 822, 833, 837, 844, 853, 854, 857, 863, 870, 875, 888, 889, 900, 944, 990, 993, 994, 1000, 1013, 1016, 1027, 1033, 1040, 1093, 1098, 1115, 1162, 1184, 1187, 1192, 1195, 1226, 1232, 1234, 1235],\
"What are the gastrointestinal complications of CF after the neonatal period (exclude liver disease and meconium ileus)?": [5, 10, 17, 36, 41, 46, 69, 72, 89, 92, 95, 97, 98, 126, 129, 130, 132, 134, 135, 148, 150, 168, 181, 182, 186, 189, 197, 202, 205, 212, 225, 226, 238, 240, 255, 288, 290, 292, 297, 298, 301, 314, 320, 322, 330, 331, 333, 350, 357, 359, 364, 370, 376, 386, 396, 398, 413, 421, 424, 428, 434, 443, 462, 466, 468, 472, 473, 475, 478, 489, 490, 510, 512, 518, 522, 550, 553, 559, 581, 582, 586, 594, 615, 616, 641, 642, 643, 649, 656, 657, 658, 659, 660, 662, 673, 676, 708, 709, 711, 715, 719, 722, 723, 724, 725, 727, 729, 730, 731, 735, 755, 756, 758, 762, 763, 764, 767, 770, 772, 783, 791, 797, 799, 809, 810, 816, 822, 834, 835, 837, 844, 867, 870, 872, 875, 882, 888, 889, 893, 896, 901, 902, 919, 928, 932, 935, 937, 938, 941, 943, 944, 970, 974, 984, 990, 991, 993, 994, 1000, 1002, 1016, 1017, 1023, 1033, 1037, 1051, 1066, 1076, 1080, 1098, 1101, 1115, 1135, 1154, 1158, 1189, 1192, 1226, 1232, 1234],\
"What is the most effective regimen for the use of pancreatic enzyme supplements in the treatment of CF patients?": [49, 89, 101, 128, 132, 135, 153, 189, 233, 238, 297, 298, 301, 330, 333, 357, 359, 370, 428, 443, 450, 506, 643, 660, 662, 688, 722, 729, 730, 731, 735, 791, 810, 816, 837, 839, 845, 882, 889, 897, 937, 938, 941, 944, 1000, 1023, 1040, 1069, 1080, 1088, 1101, 1103, 1115, 1187, 1234],\
"What is the frequency of CF in non-Caucasian populations?": [13, 39, 67, 69, 104, 130, 189, 197, 221, 226, 237, 247, 258, 262, 276, 322, 325, 333, 342, 343, 350, 365, 370, 392, 431, 464, 465, 473, 478, 503, 510, 512, 514, 586, 590, 654, 671, 682, 692, 704, 713, 729, 731, 735, 764, 774, 788, 843, 845, 871, 880, 881, 882, 888, 898, 908, 942, 946, 968, 1000, 1033, 1040, 1083, 1093, 1114, 1144, 1156, 1166, 1194, 1195],\
"What alternative techniques other than the classical Gibson-Cooke quantitative pilocarpine iontophoresis test (with titrimetric analysis of chloride) are available for sweat testing; what are their relative advantages and disadvantages?": [37, 65, 76, 77, 94, 135, 225, 235, 236, 247, 261, 277, 297, 359, 403, 404, 465, 471, 552, 627, 637, 638, 721, 773, 795, 817, 818, 825, 846, 916, 933, 941, 944, 995, 1000, 1023, 1052, 1186, 1234],\
"Is Vitamin D metabolism normal in CF patients?":[46, 296, 301, 322, 370, 392, 603, 941, 998, 1106, 1107, 1108, 1115, 1184, 1190],\
"What is known about prolactin in CF patients?":[406, 505],\
"Does secretory IgA protect CF patients against bacterial colonization or infection?":[1, 11, 55, 81, 160, 188, 223, 228, 347, 370, 401, 432, 447, 505, 509, 577, 590, 767, 917, 987, 1170, 1228, 1229],\
"What is the relationship of allergy or hypersensitivity to lung disease in CF patients?": [11, 23, 55, 187, 206, 211, 223, 228, 229, 333, 341, 347, 358, 369, 382, 394, 401, 402, 432, 485, 488, 505, 513, 547, 550, 552, 577, 590, 607, 613, 626, 631, 632, 716, 767, 771, 790, 793, 806, 812, 819, 860, 904, 905, 917, 941, 964, 990, 1003, 1005, 1007, 1013, 1048, 1060, 1099, 1134, 1163, 1164, 1169, 1171, 1192, 1237],\
"What is the pathophysiologic role of circulating antibodies to Pseudomonas aeruginosa in CF patients?": [1, 6, 8, 11, 62, 79, 80, 81, 160, 177, 178, 188, 200, 223, 228, 282, 346, 369, 370, 394, 397, 415, 432, 447, 513, 577, 588, 590, 668, 778, 784, 790, 812, 833, 860, 865, 890, 905, 983, 986, 987, 988, 989, 1086, 1090, 1091, 1095, 1170, 1171, 1173, 1203],\
"What is the incidence of and treatment for hypertrophic osteoarthropathy in CF patients?":[59, 183, 370, 579, 803, 833, 1000, 1017, 1033, 1097, 1232],\
"Are there abnormalities of taste in CF patients?":[268, 324, 449, 992, 1191],\
"What are the effects of CF on the development and/or function of the brain and central nervous system?":[145, 180, 270, 272, 362, 467, 595, 667, 728, 782, 787, 985, 1018, 1019, 1118],\
"Is oxygen transport by red blood cells abnormal in CF patients?":[52, 68, 135, 140, 190, 392, 416, 538, 539, 751, 757],\
"Is there an increased incidence of dental problems (eg, caries or periodontal disease) in CF patients?":[9, 40, 43, 75, 454, 455, 520, 526, 527, 673, 883, 1087],\
"What abnormalities of skeletal muscle function or structure have been found in CF patients?":[12, 30, 43, 192, 257, 322, 603, 606, 1097],\
"What animal models are available which are relevant to CF?":[78, 114, 122, 123, 137, 192, 209, 270, 277, 282, 309, 311, 322, 359, 370, 400, 435, 436, 440, 442, 494, 498, 504, 505, 533, 536, 571, 742, 745, 789, 955, 1016, 1091, 1092, 1121, 1143, 1156, 1158, 1197, 1199, 1200, 1204, 1223],\
"Do CF patients have normal intelligence?":[113, 145, 180, 272, 422, 467, 489, 550, 586, 722, 724, 873, 999, 1000, 1020, 1023, 1033, 1233],\
"What is the prognosis for survival of patients with CF?":[17, 43, 111, 130, 135, 136, 148, 181, 185, 189, 193, 200, 213, 226, 238, 258, 333, 342, 354, 370, 377, 392, 429, 434, 446, 465, 472, 473, 479, 489, 492, 503, 510, 514, 550, 559, 586, 596, 599, 607, 611, 643, 653, 661, 671, 687, 692, 705, 722, 724, 729, 731, 735, 763, 764, 767, 778, 783, 788, 804, 806, 822, 824, 826, 837, 838, 839, 842, 845, 856, 858, 859, 879, 883, 888, 889, 908, 910, 914, 915, 926, 930, 934, 940, 941, 944, 946, 952, 990, 1000, 1014, 1023, 1031, 1033, 1040, 1066, 1071, 1093, 1147, 1151, 1186, 1188, 1192, 1195, 1226, 1227, 1232, 1234],\
"What are the unusual manifestations of CF (other than lung disease or exocrine pancreatic insufficiency)?":[1, 3, 4, 8, 9, 11, 13, 15, 17, 21, 29, 30, 32, 33, 40, 41, 45, 46, 50, 56, 57, 58, 59, 60, 69, 78, 88, 92, 94, 95, 97, 98, 100, 103, 105, 109, 115, 116, 118, 119, 121, 122, 124, 128, 134, 135, 139, 147, 163, 166, 170, 173, 174, 181, 182, 183, 186, 189, 199, 202, 204, 211, 226, 237, 240, 241, 242, 243, 244, 248, 250, 256, 259, 261, 263, 264, 265, 266, 267, 268, 272, 274, 275, 276, 278, 279, 281, 283, 286, 287, 294, 297, 300, 301, 314, 317, 322, 331, 333, 339, 348, 351, 352, 353, 354, 355, 359, 361, 362, 364, 370, 376, 381, 385, 392, 395, 396, 398, 405, 412, 413, 416, 422, 423, 426, 428, 431, 434, 443, 454, 455, 466, 468, 473, 474, 475, 478, 485, 486, 489, 508, 512, 538, 545, 549, 550, 551, 552, 553, 559, 562, 579, 582, 586, 594, 598, 601, 603, 611, 615, 626, 641, 642, 643, 648, 659, 667, 673, 682, 683, 684, 688, 690, 694, 695, 700, 704, 714, 719, 720, 722, 724, 725, 727, 728, 729, 731, 732, 733, 735, 751, 752, 756, 759, 762, 763, 764, 767, 768, 770, 771, 772, 773, 779, 781, 782, 784, 787, 788, 791, 794, 796, 797, 798, 799, 801, 803, 808, 809, 822, 833, 834, 835, 836, 838, 844, 854, 859, 866, 867, 868, 870, 872, 875, 880, 882, 883, 888, 893, 894, 896, 897, 900, 906, 913, 914, 935, 941, 944, 947, 965, 974, 982, 985, 990, 992, 993, 997, 998, 1000, 1018, 1019, 1023, 1033, 1040, 1041, 1043, 1047, 1051, 1054, 1056, 1057, 1058, 1063, 1080, 1085, 1091, 1093, 1095, 1097, 1098, 1103, 1106, 1107, 1108, 1115, 1116, 1118, 1119, 1125, 1134, 1177, 1184, 1186, 1189, 1191, 1192, 1216, 1217, 1219, 1226, 1232, 1234, 1235],\
"What factors are responsible for the appearance of mucoid strains of Pseudomonas aeruginosa in CF patients?":[7, 160, 161, 176, 177, 200, 260, 265, 370, 451, 479, 505, 589, 590, 763, 778, 874, 884, 912, 987, 1065, 1071, 1086, 1089, 1090, 1091, 1234, 1238],\
"What is the role of viral infection in the lung disease of CF patients?":[370, 443, 457, 590, 614, 668, 678, 679, 702, 945, 990, 1091, 1134, 1144],\
"What is the role of fungi in the pathogenesis of lung disease in CF patients?":[187, 223, 228, 229, 333, 369, 370, 382, 394, 401, 432, 438, 485, 513, 550, 590, 631, 632, 668, 722, 812, 819, 833, 860, 945, 990, 1005, 1007, 1015, 1025, 1032, 1060, 1071, 1134, 1163, 1169, 1180, 1234],\
"What is the role of bacteria other than Pseudomonas aeruginosa,Staphylococcus aureus, or Haemophilus influenzae in the pathogenesis of lung disease in CF patients?":[8, 61, 85, 110, 135, 148, 152, 160, 200, 238, 271, 330, 346, 370, 384, 427, 505, 554, 555, 577, 586, 590, 722, 731, 763, 769, 922, 944, 945, 952, 983, 990, 1000, 1015, 1033, 1071, 1077, 1086, 1090, 1091, 1112, 1118, 1173, 1181, 1227, 1232, 1234],\
"What is the role of aerosols in the treatment of lung disease in CF patients?":[25, 31, 90, 93, 132, 135, 148, 152, 159, 189, 195, 197, 238, 253, 297, 321, 326, 327, 330, 331, 333, 359, 370, 427, 438, 458, 542, 543, 546, 550, 551, 586, 592, 722, 724, 729, 731, 734, 826, 837, 845, 879, 882, 889, 904, 912, 937, 941, 944, 952, 963, 990, 1000, 1003, 1040, 1078, 1092, 1150, 1188, 1227, 1232, 1234]
                              }

        def mrr(self):
                if not self.rs:
                        return
                self.rs = (np.asarray(r).nonzero()[0] for r in self.rs)
                m =  np.mean([1. / (r[0] + 1) if len(r) else 0. for r in self.rs])
                print('\nMrr para as consultas:', m,'\n')
                
        def p_at_n(self, r, k):
                if k >= 1:
                        r = r[:k] 
                        if len(r) < k:
                                raise ValueError('Relevance score length < k')
                        return np.mean(np.array(r))

        def ap(self, r):
                out = [self.p_at_n(r, k + 1) for k in range(len(r)) if r[k]]
                if not out:
                        return 0.
                return np.mean(np.array(out))

        def Map(self, rs):
                return np.mean([self.ap(r) for r in [rs]])

        def tl(self, query, rs, t='v'):
                if query in self.dict:
                        rel = self.dict[query]
                s = []
                for i in rs:
                        if t== 'v' and i[1] in rel:
                                s.append(1)
                        elif t== 'w' and i[0] in rel:
                                s.append(1)
                        else:
                                s.append(0)
                self.rs = list(self.rs)
                self.rs.append(s)
                m = self.Map(s)
                print('\nMap para essa consulta:', m)
                
                

