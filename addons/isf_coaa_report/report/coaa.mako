<html>
<head>
    <style type="text/css">
        ${css}

.row { 
    width: "100%";
    border-top: thin solid  #ffffff ;
}

.std_text {
    font-size:12;
}

tfoot.totals tr:first-child td{
    padding-top: 15px;
}


.label {
    width: 80%;
}

.currency {
    width: "10%";
    text-align: right;
    white-space: nowrap;
}
    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <h1>Chart of Analytic Accounts</h1>
    <div class="no_bloc"></div>

    <%
    level = -1
    %>
    <table style="width: 100%">
    %for account, alevel in lines():
        <tr class="row" style="border-top: 0.5px solid blue;">
            <td class="label">
        %for l in range(alevel):
            &nbsp;&nbsp;
        %endfor
        <% level = alevel %>
            ${account['code']} ${account['name']}
           </td>
            <td class="currency">
                ${account['currency_id']['name']}
            </td>
            <td class="currency">
                ${account['type']}
            </td>
        <tr>
    %endfor
    </table>


</body>
</html>
