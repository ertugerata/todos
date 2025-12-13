INSERT INTO _collections (id, system, name, type, fields, indexes, listRule, viewRule, createRule, updateRule, deleteRule, options, created, updated)
VALUES (
    '{collection_id}',
    0,
    'todos',
    'base',
    '{schema_json}',
    '[]',
    '@request.auth.id != "" && user = @request.auth.id',
    '@request.auth.id != "" && user = @request.auth.id',
    '@request.auth.id != "" && user = @request.auth.id',
    '@request.auth.id != "" && user = @request.auth.id',
    '@request.auth.id != "" && user = @request.auth.id',
    '{{}}',
    strftime('%Y-%m-%d %H:%M:%S.000Z', 'now'),
    strftime('%Y-%m-%d %H:%M:%S.000Z', 'now')
);
