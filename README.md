# GPS and IMU sensor unit
<h1>Moduly</h1>
<h1>1.týždeň</h1>
<h2>Rozdelenie úloh</h2>
<p>realizácia zapojenia a program pre zobrazenie výstupných hodnôt jednotlivých modulov</p>
<ol></ol>
    <li>Jozek - Gyroskop</li>
    <li>Kancian - Akcelerátor</li>
    <li>Nádvorník - GPS modul NEO-6M</li>
</ol>
<h2>MPU5060</h2>
<p>senzor zodpovedný za meranie zrýchlenia a uhlu naklonenia v troch rozmeroch</p>
<h3>Vstúpy/Výstupy</h3>
<table>
<tr>
    <th>IN</th>
    <th>3v3</th>
  </tr>
  <tr>
    <th>GND</th>
    <th>GND</th>
  </tr>
  <tr>
    <th>OUT</th>
    <th>SCL</th>
  </tr>
   <tr>
    <th>OUT</th>
    <th>SDA</th>
  </tr>
</table>
<h2>NEO-6M</h2>
<p>NEO-6M je jednoduchý GPS príjmač</p>
<h3>Vstúpy/Výstupy</h3>
<table>
<tr>
    <th>IN</th>
    <th>3v3</th>
  </tr>
  <tr>
    <th>GND</th>
    <th>GND/th>
  </tr>
  <tr>
    <th>IN</th>
    <th>Rx/th>
  </tr>
  <tr>
    <th>OUT</th>
    <th>Tx/th>
  </tr>
</table>
  <h2>OLED</h2>
  <p>OLED displej veĽkosti 128x64</p>
  <h3>Vstúpy/Výstupy</h3>
<table>
<tr>
    <th>IN</th>
    <th>3v3</th>
  </tr>
  <tr>
    <th>GND</th>
    <th>GND</th>
  </tr>
  <tr>
    <th>OUT</th>
    <th>SCL</th>
  </tr>
   <tr>
    <th>OUT</th>
    <th>SDA</th>
  </tr>
</table>
  <h2>Akcelerátor</h2>
  <p>*Diagram zapojenia pre zistenie meraných hodnôt/výstupné parametre*</p>
  <p>*Tabuľka pre zapojenie modulu na mikropočítać*</p>
<table>
<tr>
    <th>3v3</th>
    <th>PIN36</th>
  </tr>
  <tr>
    <th>GND</th>
    <th>PIN3</th>
  </tr>
  <tr>
    <th>SCL</th>
    <th>GP3</th>
  </tr>
   <tr>
    <th>SDA</th>
    <th>GP2</th>
  </tr>
</table>
  <h2>Gyroskop</h2>
  <p>*Diagram zapojenia pre zistenie meraných hodnôt/výstupné parametre*</p>
  <p>*Tabuľka pre zapojenie modulu na mikropočítać*</p>
<table>
<tr>
    <th>IN</th>
    <th>3v3</th>
  </tr>
  <tr>
    <th>GND</th>
    <th>GND</th>
  </tr>
  <tr>
    <th>OUT</th>
    <th>SCL</th>
  </tr>
   <tr>
    <th>OUT</th>
    <th>SDA</th>
  </tr>
</table>
  <h2>GPS modul NEO-6M</h2>
  <p>*Diagram zapojenia pre zistenie meraných hodnôt/výstupné parametre*</p>
  <p>*Tabuľka pre zapojenie modulu na mikropočítać*</p>
<table>
<tr>
    <th>IN</th>
    <th>3v3</th>
  </tr>
  <tr>
    <th>GND</th>
    <th>GND</th>
  </tr>
  <tr>
    <th>OUT</th>
    <th>SCL</th>
  </tr>
   <tr>
    <th>OUT</th>
    <th>SDA</th>
  </tr>
</table>
  <h1>2.týždeň</h1>
  <h2>Rozdelenie úloh</h2>
  <h2>Spojenie individualných modulov</h2>
  <p>*Diagram kompletného zapojenia*</p>
