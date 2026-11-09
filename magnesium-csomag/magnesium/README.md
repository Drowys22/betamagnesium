# Magnesium

Parancssoros eszköz fejlesztőknek: látványos animációk és időt spórló parancsok.

## Telepítés

```bash
pip install magnesium
```

## Használat

```bash
magnesium              # interaktív mód indító animációval
magnesium --no-anim    # animáció nélkül
magnesium sysinfo      # egyetlen parancs futtatása
```

## Új parancs hozzáadása

`src/magnesium/commands.py`:

```python
@command("hello", "Köszönés")
def cmd_hello(args):
    print("Szia!")
```

## Szponzorok

A szponzorok az indító animációban jelennek meg. Lásd: `src/magnesium/sponsors.py`.

## Fejlesztés

```bash
pip install -e .
```
