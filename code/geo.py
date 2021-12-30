'''
NFHS Data Parser - Compendium offsets
Author: Akshay Ranjan <akshay@mlcfoundation.org.in>
MLC Foundation, India
December, 2021
'''

# List of states
States = {
    'Punjab': 
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 20
    }, 
    'Haryana':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 22
    },
    'Uttarakhand':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 13
    },
    'Uttar_Pradesh':
    {
        'State':
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 75
    },
    'Madhya_Pradesh':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 51
    },
    'Rajasthan':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 33
    },
    'Bihar':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 38
    },
    'Chhattisgarh':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 20
    },
    'Jharkhand':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 24
    },
    'Odisha':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 30
    },
    'Maharashtra':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 36
    },
    'Telangana':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 31
    },
    'Andhra_Pradesh':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 13
    },
    'Goa':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 2
    },
    'Karnataka':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 30
    },
    'Tamil_Nadu':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 32
    },
    'Kerala':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 14
    },
    'West_Bengal':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 20
    },
    'Sikkim':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 4
    },
    'Arunachal_Pradesh':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 20
    },
    'Assam':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 33
    },
    'Manipur':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 9
    },
    'Mizoram':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 8
    },
    'Meghalaya':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 11
    },
    'Nagaland':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 11
    },
    'Tripura':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 8
    },
    'NCT_Delhi':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 11
    },
    'Andaman_Nicobar_Islands':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 3
    },
    'Dadra_Nagar_Haveli_Daman_Diu':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 3
    },
    'Jammu_Kashmir':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 20
    },
    'Ladakh':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 2
    },
    'Puducherry':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'District':
        {
            'Begin': 11,
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 4
    },
    'Chandigarh':
    {
        'State': 
        {
            'Begin': 5, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 0
    },
    'Lakshadweep':
    {
        'State': 
        {
            'Begin': 2, 
            'Sample_Info': 1,
            'Data_Begin': 2,
            'Data_Span': 4,
        },
        'Districts': 0
    }
}