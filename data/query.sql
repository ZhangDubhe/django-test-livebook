select  c.CUI, "symptom",c.STR from mrconso c, mrsty s where c.CUI = s.CUI and s.TUI = "T184"
;
select c.STR, c.CUI from mrconso c, mrsty s where c.CUI = s.CUI and s.TUI = "T047"
;