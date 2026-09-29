package storage

import (
    "context"
    "database/sql"
    "database/sql/driver"
    "io"
    "strings"
    "sync"
    "testing"
    "time"

    "github.com/tobilg/ai-observer/internal/api"
)

type fakeDB struct { mu sync.Mutex; widgets map[string]widgetRow }
type widgetRow struct { id, dashboard, typ, title string; col, row, colspan, rowspan int64; config string; created, updated time.Time }
type fakeDriver struct { db *fakeDB }
type fakeConn struct { db *fakeDB }
type fakeResult int64
type fakeRows struct { columns []string; values [][]driver.Value; at int }

func (fakeResult) LastInsertId() (int64,error) { return 0,nil }
func (fakeResult) RowsAffected() (int64,error) { return 1,nil }
func (d fakeDriver) Open(string) (driver.Conn,error) { return fakeConn{d.db},nil }
func (c fakeConn) Close() error { return nil }
func (c fakeConn) Begin() (driver.Tx,error) { return nil, nil }
func (c fakeConn) Prepare(string) (driver.Stmt,error) { return nil, nil }
func (c fakeConn) ExecContext(_ context.Context, q string, args []driver.NamedValue) (driver.Result,error) {
    c.db.mu.Lock(); defer c.db.mu.Unlock();
    if strings.Contains(q,"INSERT INTO dashboard_widgets") {
        vals:=make([]any,len(args)); for i,a:=range args { vals[i]=a.Value }
        cfg,_:=vals[8].(string); created,_:=vals[9].(time.Time); updated,_:=vals[10].(time.Time)
        c.db.widgets[vals[0].(string)] = widgetRow{id:vals[0].(string),dashboard:vals[1].(string),typ:vals[2].(string),title:vals[3].(string),col:vals[4].(int64),row:vals[5].(int64),colspan:vals[6].(int64),rowspan:vals[7].(int64),config:cfg,created:created,updated:updated}
        return fakeResult(1),nil
    }
    if strings.Contains(q,"UPDATE dashboard_widgets") {
        id:=args[12].Value.(string); dash:=args[13].Value.(string); w,ok:=c.db.widgets[id]; if !ok || w.dashboard!=dash { return fakeResult(0),nil }
        if v:=args[0].Value.(string); v!="" { w.title=v }; if v:=args[2].Value.(int64); v>0 { w.col=v }; if v:=args[4].Value.(int64); v>0 { w.row=v }; if v:=args[6].Value.(int64); v>0 { w.colspan=v }; if v:=args[8].Value.(int64); v>0 { w.rowspan=v }; w.config=args[10].Value.(string); w.updated=args[11].Value.(time.Time); c.db.widgets[id]=w; return fakeResult(1),nil
    }
    return fakeResult(1),nil
}
func (c fakeConn) QueryContext(_ context.Context, q string, args []driver.NamedValue) (driver.Rows,error) {
    c.db.mu.Lock(); defer c.db.mu.Unlock();
    if strings.Contains(q,"FROM dashboard_widgets WHERE id = ? AND dashboard_id = ?") { id:=args[0].Value.(string); dash:=args[1].Value.(string); w,ok:=c.db.widgets[id]; if !ok || w.dashboard!=dash { return &fakeRows{columns: []string{"id"}},nil }; return &fakeRows{columns: []string{"id","dashboard_id","widget_type","title","grid_column","grid_row","col_span","row_span","config","created_at","updated_at"},values:[][]driver.Value{{w.id,w.dashboard,w.typ,w.title,w.col,w.row,w.colspan,w.rowspan,w.config,w.created,w.updated}}},nil }
    return &fakeRows{columns: []string{"id"}},nil
}
func (r *fakeRows) Columns() []string { return r.columns }
func (r *fakeRows) Close() error { return nil }
func (r *fakeRows) Next(dest []driver.Value) error { if r.at>=len(r.values) { return io.EOF }; copy(dest,r.values[r.at]); r.at++; return nil }

func TestUpdateWidgetRejectsWidgetFromAnotherDashboard(t *testing.T) {
    mem:=&fakeDB{widgets:map[string]widgetRow{}}; sql.Register("crud_scope_fake", fakeDriver{mem}); db,err:=sql.Open("crud_scope_fake",""); if err!=nil { t.Fatal(err) }; defer db.Close(); store:=&DuckDBStore{db:db}
    owner:=&api.CreateDashboardRequest{Name:"Owner"}; other:=&api.CreateDashboardRequest{Name:"Other"}; _=owner; _=other
    // UUID parent IDs are enough for this focused adapter; the child is inserted through production CreateWidget.
    widgetID:="widget-1"; mem.widgets[widgetID]=widgetRow{id:widgetID,dashboard:"owner",typ:"table",title:"Original",col:1,row:1,colspan:1,rowspan:1,config:`{}`}
    _,err=store.UpdateWidget(context.Background(),"other",widgetID,&api.UpdateWidgetRequest{Title:"Cross dashboard"}); if err==nil { t.Fatal("expected wrong-parent update to fail") }
    if mem.widgets[widgetID].title!="Original" { t.Fatal("wrong-parent request changed owner widget") }
}
