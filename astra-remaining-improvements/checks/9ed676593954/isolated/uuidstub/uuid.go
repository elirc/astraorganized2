package uuid

type UUID string

func New() UUID { return "generated" }

func (u UUID) String() string { return string(u) }
